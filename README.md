# Microsoft Foundry Agent Workshop

เวิร์กช็อปภาคปฏิบัตินี้พาผู้เรียนพัฒนา **Fabrikam Service Operations Agent** แบบต่อเนื่อง ตั้งแต่เตรียม Microsoft Foundry project ไปจนถึง Agent Framework และ multi-agent orchestration โดยใช้ project และ codebase เดิมตลอดวัน

> **License:** เนื้อหาต้นฉบับของเวิร์กช็อปนี้เป็นลิขสิทธิ์ของ Amaround Co., Ltd. แบบ All rights reserved ส่วนเนื้อหาและโค้ดที่ดัดแปลงจาก MicrosoftLearning อยู่ภายใต้ MIT License ตาม [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)

## ก่อนเริ่ม

- สำหรับ IT Admin: ทำตาม [IT Admin Environment Setup](./IT_ADMIN_ENVIRONMENT_SETUP.md) เพื่อเตรียม Azure account, Resource group, RBAC, Network และ GitHub Codespaces
- สำหรับผู้เรียน: ทำตาม [Student Environment Validation](./STUDENT_ENVIRONMENT_VALIDATION.md) เพื่อตรวจ GitHub, Codespace, Azure account, Role และ Microsoft Foundry ก่อนเริ่ม Exercise
- ผู้ดูแลระบบต้องจัดเตรียม Azure account และ resource group แยกสำหรับผู้เรียนแต่ละคน
- ให้ใช้เฉพาะ resource group ที่ได้รับมอบหมาย
- ต้องยืนยัน region, model, quota, RBAC และ network ก่อนวันอบรม
- GitHub Codespaces มี included usage จำกัดตามประเภทบัญชี จึงต้องตรวจสอบสิทธิ์ก่อนเริ่มอบรม
- ถ้าใช้ Codespaces ไม่ได้ ให้ใช้ VS Code พร้อม Dev Containers เป็น fallback

## ดาวน์โหลดไฟล์เตรียมแบบครั้งเดียว

- ผู้เรียนสามารถดาวน์โหลดไฟล์ตัวอย่างของ Exercise 1-7 แบบครั้งเดียวได้ที่ [student-prep-files.zip](./exercises/student-prep-files.zip)
- หลังดาวน์โหลดให้แตกไฟล์ zip โดยคงโครงสร้างโฟลเดอร์เดิม เพื่อหาไฟล์ตามขั้นตอนแต่ละ Exercise ได้ง่าย
- ผู้สอนสามารถ rebuild ไฟล์นี้ได้ด้วยคำสั่ง `bash scripts/build_student_prep_zip.sh`

## เริ่ม Codespace

1. เปิด repository นี้ใน GitHub แล้วเลือก **Code > Codespaces > Create codespace on current branch**
2. รอให้ bootstrap ติดตั้ง dependencies ลงใน `.venv` โดยอัตโนมัติ
3. เปิด Terminal แล้วรัน:

   ```bash
   python -m service_ops check
   ```

4. ตรวจว่า Python, Git, Azure CLI และ Python packages แสดงสถานะพร้อมใช้งาน

> **⚠️ Note:** คำสั่งตรวจสอบอาจแสดง `ACTION` สำหรับ Azure sign-in และค่าใน `.env` จนกว่าจะทำ Exercise 1 เสร็จ นี่เป็นผลลัพธ์ที่คาดไว้ ไม่ใช่การติดตั้งล้มเหลว

## Exercises

| ลำดับ | Exercise | สถานะในชุดงานนี้ |
|---|---|---|
| 1 | [เตรียม Microsoft Foundry project](./exercises/01-prepare-foundry-project/README.md) | พร้อมใช้งาน |
| 2 | [สร้าง Service Operations Agent](./exercises/02-build-service-operations-agent/README.md) | พร้อมใช้งาน |
| 3 | [เชื่อมต่อ Agent กับ MCP](./exercises/03-extend-agent-with-mcp/README.md) | พร้อมใช้งาน |
| 4 | [เพิ่ม Foundry IQ](./exercises/04-add-foundry-iq/README.md) | พร้อมใช้งาน; ต้องผ่าน environment gate |
| 5 | [สร้าง visual workflow](./exercises/05-build-foundry-workflow/README.md) | พร้อมใช้งาน; Preview และ retire 1 Dec 2026 |
| 6 | [สร้าง code-first Agent Framework agent](./exercises/06-build-agent-framework-agent/README.md) | พร้อมใช้งาน |
| 7 | [สร้าง multi-agent solution](./exercises/07-build-multi-agent-solution/README.md) | พร้อมใช้งาน |
| Optional | [เผยแพร่ไปยัง Teams และ Microsoft 365 Copilot](./exercises/optional-teams-copilot/README.md) | `ต้องตรวจสอบก่อนเริ่มอบรม` |

## Application commands

```bash
python -m service_ops check
python -m service_ops agent
python -m service_ops mcp-server
python -m service_ops mcp-agent --source local --prompt "..."
python -m service_ops workflow --mode local
python -m service_ops multi-agent --feedback "..."
```

Starter code มี `TODO Exercise ...` ให้ผู้เรียนเติมตามลำดับ ห้ามข้ามไป copy private instructor solution ทุก Exercise ใช้ package `service_ops`, project และ model deployment เดิม

## การเก็บข้อมูลสำคัญ

- คัดลอก `.env.example` เป็น `.env` แล้วใส่เฉพาะชื่อและ endpoint ที่ Exercise ระบุ
- ห้าม commit `.env`, access token, key, tenant ID, subscription ID หรือข้อมูล production
- ใช้ `az login --use-device-code` และ `AzureCliCredential`; repository นี้ไม่ใช้ API key

## ตรวจงานใน repository

```bash
bash scripts/validate.sh
```

คำสั่งนี้ตรวจรูปแบบโค้ด, compilation, unit tests, JSON, local Markdown links, secrets ที่พบบ่อย และ dependency consistency โดยไม่เรียกใช้ Azure quota
