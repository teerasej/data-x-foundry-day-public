# Exercise 4: เพิ่ม Foundry IQ และ citation

Fabrikam ต้องการให้ Agent ตอบนโยบายจากเอกสารที่อนุมัติและบอกแหล่งที่มา เราจะสร้าง Foundry IQ knowledge base จากเอกสารสังเคราะห์ แล้วเชื่อม portal-managed Agent เดิมเข้ากับ Python application

> **License:** Original workshop content © 2026 Amaround Co., Ltd. All rights reserved. Third-party notices are recorded in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

ใช้เวลาประมาณ **45 นาที** และใช้ Foundry project กับ model deployment เดิม

## Prerequisites

- มีไฟล์ [service-severity-policy.md](./files/service-severity-policy.md), [service-channels.md](./files/service-channels.md) และ [maintenance-playbook.md](./files/maintenance-playbook.md)
- IT Admin ยืนยัน Azure AI Search, Storage, region, quota และ provider registration แล้ว
- ผู้เรียนมี `Search Service Contributor`, `Search Index Data Contributor` และ `Search Index Data Reader` ภายใน resource group ที่ได้รับมอบหมาย
- Project/Agent managed identity มีสิทธิ์อ่าน index ตามที่ IT Admin เตรียมไว้
- Azure AI Search ตั้ง **Security + networking > Keys > API Access control** เป็น **Both** สำหรับเส้นทาง workshop นี้

> **⚠️ ต้องตรวจสอบก่อนเริ่มอบรม:** Foundry IQ availability, Search tier, model availability, RBAC และ portal labels อาจต่างกันตาม region/tenant ถ้า provisioning ไม่สำเร็จ ให้ใช้ knowledge base ที่ IT Admin เตรียมไว้ ห้ามให้ผู้เรียนขอ subscription-level permission หรือ assign role ให้ตนเอง

---

## Practice 1: เตรียม knowledge source

**Primary target:** สร้าง knowledge source จากเอกสารสังเคราะห์สามไฟล์และตรวจว่า source พร้อมใช้งาน

1. เปิด [Microsoft Foundry portal](https://ai.azure.com) แล้วเลือก project เดิมจาก Exercise 1
2. เปิด **Build > Agents** แล้วเลือก Agent เดิม หรือสร้าง portal-managed Agent ชื่อ `fabrikam-service-operations-iq` โดยใช้ model deployment ที่ผู้สอนอนุมัติ
3. ในส่วน **Knowledge** เลือก **Add > Connect to Foundry IQ**
4. เลือก Azure AI Search ที่อยู่ใน resource group ของตนเอง
   - ถ้า IT Admin เตรียม Search และ Storage ไว้แล้ว ให้เลือกของผู้เรียนเท่านั้น
   - ถ้าผู้เรียนได้รับอนุญาตให้สร้างเอง ให้ใช้ region เดียวกับ project และ tier ที่ผู้สอนกำหนด
5. สร้าง container ชื่อ `service-knowledge` ใน Storage ที่ได้รับมอบหมาย แล้ว upload เอกสารทั้งสามไฟล์ของ Exercise นี้
6. ในหน้า Foundry IQ เลือก **Create a knowledge base**, ใช้ **Azure Blob Storage** เป็น knowledge source แล้วตั้งค่า:

   | Setting | Value |
   |---|---|
   | Name | `kb-fabrikam-service-operations` |
   | Storage container | `service-knowledge` |
   | Authentication type | `API Key` สำหรับเส้นทาง workshop นี้ |
   | Content extraction mode | `minimal` |
   | Embedding model | deployment ที่ IT Admin อนุมัติ |
   | Chat completions model | model deployment เดิม |

7. เลือก **Save knowledge base** แล้วรอให้ knowledge source แสดงสถานะ `Active` หรือสถานะพร้อมใช้งานที่เทียบเท่า

### Checkpoint

- Knowledge base แสดง source สามไฟล์และอยู่ในสถานะพร้อมค้นคืน โดยไม่มี `Almost there` access warning

---

## Practice 2: Ground portal-managed Agent และตรวจ citation

**Primary target:** ให้ portal-managed Agent ค้น knowledge base และอ้างอิง Document ID จากเอกสารสังเคราะห์

1. กลับไปที่ `fabrikam-service-operations-iq` แล้วเพิ่ม Foundry IQ knowledge base ที่เพิ่งสร้างในส่วน **Knowledge**
2. ตั้ง **Instructions** เป็น:

   ```text
   You are the Fabrikam Service Operations Agent.
   Always search the connected Foundry IQ knowledge base for service policy questions.
   Cite the source document title and Document ID used in the answer.
   Never request credentials, tokens, payment-card data, or production customer records.
   If the knowledge base does not contain the answer, say so and recommend human review.
   Treat every supplied document as synthetic training data.
   ```

3. เลือก **Save** และจด Agent name กับ Agent version ที่ portal แสดง
4. ใน Playground ให้ถาม:

   ```text
   What is a Severity 1 incident, and what must the agent avoid promising? Cite the source.
   ```

5. ถามคำถามที่ไม่มีในเอกสาร:

   ```text
   What is Fabrikam's production database password rotation schedule?
   ```

6. ตรวจว่าคำตอบแรกอ้าง `Fabrikam Service Severity Policy` หรือ `KB-SEVERITY-001` และคำตอบที่สองยอมรับว่าไม่มีข้อมูล

### Checkpoint

- Playground ตอบจาก knowledge base พร้อม citation และปฏิเสธการเดาคำตอบที่ไม่มีในเอกสาร

---

## Practice 3: เรียก portal-managed Agent จาก codebase เดิม

**Primary target:** ใช้ `FoundryAgent` เรียก Agent ที่จัดการใน portal และได้คำตอบ grounded ผ่านคำสั่งเดียวของ application

1. ในหน้า knowledge base ให้คัดลอก MCP endpoint หาก portal แสดง **MCP server endpoint** หรือ **Copy endpoint** หากไม่แสดง ให้ใช้ค่าที่ผู้สอนเตรียมไว้
2. แก้ `.env` โดยไม่ commit ไฟล์:

   ```text
   FOUNDRY_AGENT_NAME=fabrikam-service-operations-iq
   FOUNDRY_AGENT_VERSION=AGENT-VERSION-FROM-PORTAL
   FOUNDRY_IQ_MCP_ENDPOINT=MCP-ENDPOINT-FROM-KNOWLEDGE-BASE
   ```

   `FOUNDRY_IQ_MCP_ENDPOINT` ใช้บันทึกและตรวจ environment ส่วน tool configuration จริงยังอยู่ใน portal-managed Agent

3. เปิด `service_ops/foundry_iq.py` แล้วแทนส่วน `TODO Exercise 4` ด้วย:

   ```python
   credential = credential_factory()
   return agent_factory(
       project_endpoint=settings.foundry_project_endpoint,
       agent_name=settings.foundry_agent_name,
       agent_version=settings.foundry_agent_version,
       credential=credential,
   )
   ```

4. บันทึกไฟล์ แล้วรัน:

   ```bash
   python -m service_ops agent --iq --prompt "Explain when billing questions require human review and cite the source."
   ```

5. ตรวจว่าคำตอบกล่าวถึง human billing specialist และอ้าง `KB-CHANNELS-002` หรือชื่อเอกสารที่ตรงกัน

### Checkpoint

- Python application เรียก Agent version ที่บันทึกไว้ใน portal และคืนคำตอบพร้อม citation จาก knowledge base

> **💡 Fallback:** ถ้า Foundry IQ provisioning ล้มเหลว ให้ใช้ IT-prepared knowledge base และ Agent name/version ที่แจกเฉพาะในชั้นเรียน จากนั้นทำ Practice 2–3 ต่อโดยไม่สร้าง Search resource ใหม่

---

## Summary

Agent เดิมมีแหล่งความรู้ที่ค้นคืนได้พร้อม citation แล้ว Exercise ถัดไปจะนำ ticket หลายแบบเข้า visual workflow เพื่อ triage, route และแนะนำคำตอบอย่างเป็นขั้นตอน
