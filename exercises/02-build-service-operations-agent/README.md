# Exercise 2: สร้าง Fabrikam Service Operations Agent

เราจะเพิ่ม Agent สองเส้นทางใน Foundry project เดิม: portal-managed agent สำหรับทดลอง File search และ Code interpreter และ code-owned Agent Framework agent สำหรับเรียก local function tools จาก application เดียวกัน

เหมือนร้านอาหารที่มีทั้งเมนูมาตรฐานเก็บไว้หน้าร้านและเชฟที่ประกอบเมนูจากโค้ด: ทั้งสองใช้ครัวเดียวกัน แต่ portal เก็บ agent definition ไว้ใน Foundry ส่วน code-owned agent ส่ง instructions และ tools จาก application ตอนรัน

> **License และค่าใช้จ่าย:** เนื้อหาต้นฉบับเป็นลิขสิทธิ์ของ Amaround Co., Ltd. แบบ All rights reserved และมีส่วนที่ดัดแปลงจาก MicrosoftLearning ภายใต้ MIT License ตาม [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md) การเรียก model ใช้ Azure quota ของสภาพแวดล้อมอบรม

## Prerequisites

- ผ่าน Checkpoint ของ Exercise 1
- Foundry project และ approved model deployment ยังทำงานอยู่
- `.env` มี `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL` และ `FOUNDRY_AGENT_NAME`
- Sample files:
  - [service-handbook.md](./files/service-handbook.md)
  - [service-metrics.csv](./files/service-metrics.csv)

---

## Practice 1: สร้างและทดสอบ portal-managed agent

**Primary target:** กำหนด portal-managed agent ให้ตอบจาก service handbook และวิเคราะห์ service metrics ได้

1. ใน Codespace Explorer เปิดโฟลเดอร์ `exercises/02-build-service-operations-agent/files`

2. คลิกขวา `service-handbook.md` และ `service-metrics.csv` แล้วเลือก **Download** เพื่อเตรียมไฟล์สำหรับอัปโหลดผ่าน browser

3. เปิด Foundry project เดิมใน [Microsoft Foundry portal](https://ai.azure.com)

4. เปิด **Build > Agents** แล้วเลือก **Create agent** ถ้า portal สร้าง draft agent ให้อัตโนมัติ ให้ใช้ draft นั้น

5. ตั้ง **Agent name** เป็น:

   ```text
   fabrikam-service-operations-agent
   ```

6. เลือก approved model deployment เดียวกับ Exercise 1

7. แทนค่า **Instructions** ด้วยข้อความนี้:

   ```text
   You are the Fabrikam Service Operations Agent.

   Your responsibilities:
   - Answer service-policy questions from the attached service handbook.
   - Analyze only the attached synthetic service metrics.
   - Cite or name the file used for factual answers.
   - Never invent a policy, metric, customer, incident, or production fact.
   - When evidence is insufficient, say what is missing and recommend human review.
   - Keep answers concise and practical.
   ```

8. ในส่วน **Tools** เลือก **Add** แล้วเพิ่ม **File search** และ **Code interpreter**

9. อัปโหลด `service-handbook.md` ให้ **File search** แล้วรอจนการทำ index เสร็จ

10. อัปโหลด `service-metrics.csv` ให้ **Code interpreter** แล้วเลือก **Save**

11. ทดสอบ handbook ด้วย prompt:

    ```text
    A customer-facing integration is unavailable for every user. Which priority applies, what is the acknowledgement target, and when should we escalate?
    ```

12. ตรวจว่าคำตอบระบุ `P1`, เป้าหมาย 15 นาที และ human escalation ตาม handbook พร้อมอ้างชื่อไฟล์

13. ทดสอบ metrics ด้วย prompt:

    ```text
    Analyze the service metrics. Which metrics miss their targets, and what should the service manager investigate first? Use only the attached CSV.
    ```

14. ตรวจว่าคำตอบพบ `resolution_rate_percent` และ `open_p1_incidents` ว่าไม่ถึงเป้าหมาย

15. เปิด **Foundry Toolkit > Microsoft Foundry Resources > Set Default Project** แล้วเลือก project เดิม

16. ใต้ **Prompt Agents** เปิด `fabrikam-service-operations-agent` และส่ง handbook prompt ซ้ำ

### Checkpoint

- Agent ตอบ policy question จาก handbook และวิเคราะห์ metrics จาก CSV ได้ใน portal
- Agent เดียวกันเปิดและตอบ handbook prompt ผ่าน Foundry Toolkit ได้

> **⚠️ Note:** ถ้า File search หรือ Code interpreter ไม่พร้อมใช้งาน ให้ผู้สอนสาธิต portal path แล้วทำ Practice 2–3 ต่อ ซึ่งใช้ local function tools กับข้อมูลชุดเดียวกัน

---

## Practice 2: ประกอบ code-owned Agent Framework agent

**Primary target:** เติม `build_agent()` ให้ `FoundryChatClient` ใช้ local handbook และ metrics tools จาก application ได้

1. เปิด `service_ops/agent.py`

2. หา block ที่เริ่มด้วย `# TODO Exercise 2`

3. ลบคำสั่ง `del ...` และ `raise NotImplementedError(...)` แล้วใส่ code ต่อไปนี้แทน:

   ```python
   credential = credential_factory()
   client = client_factory(
       project_endpoint=settings.foundry_project_endpoint,
       model=settings.foundry_model,
       credential=credential,
   )
   return agent_factory(
       client=client,
       name=settings.foundry_agent_name or "fabrikam-service-operations-agent",
       instructions=AGENT_INSTRUCTIONS,
       tools=[search_service_handbook, list_service_metrics],
   )
   ```

4. บันทึกไฟล์ แล้วตรวจ code style และ deterministic tests:

   ```bash
   python -m ruff check service_ops tests
   python -m pytest
   ```

5. ตรวจความเข้าใจใน code:

   - `AzureCliCredential` ใช้ session จาก `az login` โดยไม่เก็บ key ใน repository
   - `FoundryChatClient` เชื่อม project endpoint กับ model deployment
   - `Agent` เก็บ instructions และ local tools ใน application
   - `search_service_handbook` และ `list_service_metrics` อ่านเฉพาะ synthetic files ของ Exercise นี้

### Checkpoint

- `build_agent()` คืน Agent ที่มี local tools สองตัว
- Ruff และ unit tests ผ่านโดยไม่เรียก Azure หรือใช้ model quota

---

## Practice 3: ทดสอบ code-owned agent และรวมผลช่วงเช้า

**Primary target:** เรียก code-owned agent จาก command line แล้วเปรียบเทียบผลกับ portal-managed agent ได้

1. ตรวจ Azure sign-in และ `.env`:

   ```bash
   python -m service_ops check --strict
   ```

2. ส่ง handbook prompt แบบ one-shot:

   ```bash
   python -m service_ops agent --prompt "For a company-wide service outage, state the priority, acknowledgement target, and escalation rule."
   ```

3. ตรวจว่า Agent เรียก `search_service_handbook` และตอบจาก synthetic handbook

4. ส่ง metrics prompt:

   ```bash
   python -m service_ops agent --prompt "Review all service metrics. Identify every missed target and recommend the first human follow-up."
   ```

5. ตรวจว่า Agent เรียก `list_service_metrics` และพบ metrics ที่ไม่ถึงเป้าหมาย

6. เปิด interactive mode:

   ```bash
   python -m service_ops agent
   ```

7. ลองถาม follow-up หนึ่งข้อ แล้วพิมพ์ `exit` เพื่อจบ

8. เปรียบเทียบสองเส้นทาง:

   | เส้นทาง | Agent definition อยู่ที่ไหน | Data/tool path |
   |---|---|---|
   | Portal-managed | Microsoft Foundry | File search และ Code interpreter ที่ตั้งค่าใน portal |
   | Code-owned | `service_ops/agent.py` | Local Python function tools ที่ application ส่งให้ model |

### Checkpoint

- Portal-managed agent และ code-owned agent ทำงานจาก Foundry project/model เดียวกัน
- Code-owned agent ตอบ policy และ metrics prompts ผ่าน `python -m service_ops agent`
- ไม่มีการเพิ่ม key, token หรือ credential ลงใน `.env` หรือ Git

---

## Summary

เราได้ Agent สองเส้นทางที่ใช้ข้อมูล synthetic ชุดเดียวกันและเห็นความต่างระหว่าง service-managed definition กับ code-owned definition แล้ว Exercise ถัดไปจะเพิ่ม remote และ local MCP tools ให้ application เดิม

> **⚠️ Note:** ยังไม่ต้องลบ Agent, model deployment, project หรือ resource group เพราะจะใช้ต่อใน Exercise 3
