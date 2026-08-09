# Exercise 1: เตรียม Microsoft Foundry project

เราจะเตรียมพื้นที่ทำงานเดียวสำหรับ Fabrikam Service Operations Agent และใช้ project กับ model deployment นี้ต่อเนื่องตลอดเวิร์กช็อป

> **License และค่าใช้จ่าย:** เนื้อหาต้นฉบับเป็นลิขสิทธิ์ของ Amaround Co., Ltd. แบบ All rights reserved และมีส่วนที่ดัดแปลงจาก MicrosoftLearning ภายใต้ MIT License ตาม [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md) การใช้ Microsoft Foundry และ GitHub Codespaces อาจมีค่าใช้จ่ายหรือ included usage จำกัด ต้องตรวจสอบสิทธิ์ก่อนเริ่มอบรม

## Prerequisites

- Codespace เปิดสำเร็จและ bootstrap ทำงานจบ
- Azure account และชื่อ resource group ที่ IT Admin มอบหมายให้
- ชื่อ region และ model ที่ผู้สอนยืนยันว่าใช้ได้
- สิทธิ์สร้าง project/model deployment หรือ IT-prepared fallback

> **⚠️ Note:** ใช้เฉพาะ resource group ที่ได้รับมอบหมาย ห้ามสร้าง resource group ใหม่หรือย้ายไปใช้ resource group ของผู้เรียนคนอื่น

---

## Practice 1: ยืนยันเครื่องมือและขอบเขต Azure

**Primary target:** ตรวจความพร้อมของ Codespace และยืนยันว่า Azure account เข้าถึง resource group ที่ได้รับมอบหมายได้

1. เปิด **Terminal** ใน Codespace แล้วรัน:

   ```bash
   python -m service_ops check
   ```

2. ตรวจว่า `Python`, `Repository virtual environment`, `Git`, `Azure CLI` และ Python imports แสดง `READY`

3. ลงชื่อเข้าใช้ Azure ด้วย device code:

   ```bash
   az login --use-device-code
   ```

4. ทำตาม URL และรหัสที่ Terminal แสดง โดยใช้บัญชีที่ IT Admin แจ้งไว้

5. ตรวจชื่อ account โดยไม่แสดง tenant หรือ subscription ID:

   ```bash
   az account show --query "{account:name,user:user.name}" --output table
   ```

6. แทน `<assigned-resource-group>` ด้วยชื่อที่ได้รับ แล้วตรวจว่าเข้าถึงได้:

   ```bash
   az group show --name <assigned-resource-group> --query "{name:name,location:location}" --output table
   ```

7. จดชื่อ project ที่จะใช้ตามรูปแบบ `foundry-serviceops-<student-number>` โดยไม่ใส่ชื่อบุคคลหรือข้อมูลลูกค้า

### Checkpoint

- คำสั่ง `python -m service_ops check` แสดง base tools เป็น `READY`
- `az group show` แสดงเฉพาะ resource group ที่ IT Admin มอบหมายได้สำเร็จ

> **💡 Tip:** ถ้า `az login` สำเร็จแต่ portal ยังไม่เห็นสิทธิ์ ให้รอสักครู่แล้ว sign out/sign in ใหม่ การกระจาย RBAC อาจใช้เวลา

---

## Practice 2: สร้าง project และทดสอบ model deployment

**Primary target:** สร้างหรือเลือก Microsoft Foundry project ใน resource group ที่กำหนด แล้วทดสอบ approved model ใน playground ได้

1. เปิด [Microsoft Foundry portal](https://ai.azure.com) แล้ว sign in ด้วยบัญชีเดียวกับ Azure CLI

2. ตรวจว่าใช้ประสบการณ์ **New Foundry** ตามที่ผู้สอนสาธิต แล้วเลือก **Start building**

3. ถ้า IT Admin เตรียม project ไว้แล้ว ให้เลือก project นั้นและข้ามไปขั้นตอนที่ 6

4. เลือกสร้าง project ใหม่ แล้วกรอกชื่อจาก Practice 1

5. เปิด **Advanced options** และตรวจค่าก่อนเลือก **Create**:

   - **Subscription:** subscription ที่ IT Admin ระบุ
   - **Resource group:** resource group ที่ได้รับมอบหมายเท่านั้น
   - **Region:** region ที่ผู้สอนยืนยัน
   - **Foundry resource:** ใช้ชื่อที่กำหนดให้หรือค่าที่ IT Admin เตรียมไว้

6. เปิด **Discover > Models** แล้วค้นหา model ที่ผู้สอนกำหนด

7. เปิด model card แล้วเปรียบเทียบอย่างน้อยสองรายการต่อไปนี้กับ model ทางเลือกที่ผู้สอนระบุ:

   - Input/output modality
   - Context window
   - Supported region หรือ deployment type
   - Limitation หรือ use case ที่ระบุใน model card

8. เลือก **Deploy** สำหรับ approved model เท่านั้น และใช้ deployment name ที่ผู้สอนกำหนด

9. ถ้ามี deployment เตรียมไว้แล้ว ให้เลือก deployment นั้นแทนการสร้างซ้ำ

10. เปิด model playground แล้วใส่ **Instructions**:

    ```text
    You are a careful service-operations assistant. Use only the information supplied in the conversation. State clearly when information is missing.
    ```

11. ส่ง prompt ต่อไปนี้:

    ```text
    A service desk wants to reduce response time without hiding unresolved incidents. Suggest three measurable checks and explain why each matters.
    ```

12. ตรวจว่าคำตอบเสนอ measurable checks และไม่อ้างข้อมูลจริงของ Fabrikam ที่ยังไม่ได้ให้

### Checkpoint

- Project อยู่ใน resource group ที่ได้รับมอบหมาย
- Approved model deployment เปิดใน playground และตอบ test prompt ได้
- ผู้เรียนอธิบายความต่างจาก model ทางเลือกได้อย่างน้อยสองข้อจาก model cards

> **⚠️ Note:** ถ้า quota หรือสิทธิ์ไม่อนุญาตให้ deploy ห้ามลอง region หรือ resource group อื่นเอง ให้ใช้ IT-prepared deployment และบันทึกว่าใช้ fallback

---

## Practice 3: เชื่อม Codespace กับ Foundry project

**Primary target:** บันทึก project endpoint และ model deployment ใน `.env` แล้วตรวจการเชื่อมต่อพื้นฐานจาก Codespace ได้

1. ใน Microsoft Foundry portal เปิด project home page แล้วคัดลอก **Project endpoint**

2. กลับมาที่ Codespace แล้วสร้าง `.env` จากไฟล์ตัวอย่าง:

   ```bash
   cp .env.example .env
   ```

3. เปิด `.env` แล้วแทนค่าต่อไปนี้:

   ```dotenv
   FOUNDRY_PROJECT_ENDPOINT=<project-endpoint>
   FOUNDRY_MODEL=<model-deployment-name>
   FOUNDRY_AGENT_NAME=fabrikam-service-operations-agent
   ```

4. บันทึกไฟล์ แล้วตรวจว่า Git จะไม่ติดตาม `.env`:

   ```bash
   git status --short
   ```

   เราไม่ควรเห็น `.env` ในรายการ

5. เปิด **Foundry Toolkit** ใน VS Code แล้วเลือก **Microsoft Foundry Resources > Set Default Project**

6. เลือก project เดียวกับที่สร้างใน Practice 2 แล้วเปิด **Models** เพื่อตรวจชื่อ deployment

7. ถ้า Foundry Toolkit ไม่แสดงผล ให้ใช้ portal เป็น fallback โดยยืนยัน project endpoint และ deployment จาก project home page

8. รัน readiness check แบบเข้มงวด:

   ```bash
   python -m service_ops check --strict
   ```

### Checkpoint

- `.env` มี project endpoint และ model deployment โดยไม่มี key หรือ credential
- `python -m service_ops check --strict` จบโดยไม่มี `ERROR` หรือ `ACTION`
- พบ model deployment ใน Foundry Toolkit หรือยืนยันผ่าน portal fallback

---

## Summary

เราเตรียม Codespace, ยืนยัน Azure boundary, สร้างหรือเลือก Foundry project, เปรียบเทียบและทดสอบ approved model แล้ว ขั้นต่อไปจะเพิ่ม portal-managed agent และ code-owned Agent Framework agent ใน project เดิม

> **⚠️ Note:** ยังไม่ต้องลบ project, model deployment หรือ resource group เพราะ Exercise ถัดไปจะใช้งานต่อ
