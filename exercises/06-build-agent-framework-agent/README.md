# Exercise 6: สร้าง code-first Agent Framework agent
 เราจะสร้าง local function tool ที่ให้ผลลัพธ์ซ้ำได้และระบุ `simulated-only` แล้วเชื่อมกับ `FoundryChatClient`


## Prerequisites

- ทำ Exercise 2 เสร็จและเข้าใจรูปแบบ `Agent(client=..., tools=[...])`
- มีไฟล์ [escalation-request.json](./files/escalation-request.json)
- ยืนยันว่า Exercise นี้ไม่เชื่อมต่อ ticketing, email, Teams หรือ production API

> **⚠️ Note:** หากเจอ error `FoundryChatClient` ที่ไม่รองรับ model รุ่นเก่า (เช่น gpt-4o) ให้ทำการ deploy model ตระกูล gpt ที่ใหม่กว่าเพิ่มเติมใน Foundry portal และแก้ค่า **FOUNDRY_MODEL** ใน `.env` ให้ตรงกับ model deployment
---

## Practice 1:  escalation tool


1. เปิด `service_ops/escalation.py` แล้วลองดูการทำงานของ function `create_escalation()`
2. สังเกตว่า ID สร้างจากค่าของ request ไม่ใช่การเรียก API ภายนอก
3. รัน:

   ```bash
   python -c "from service_ops.escalation import create_escalation; print(create_escalation('SR-2001', 'Complete outage', 'high'))"
   ```

4. รันคำสั่งเดิมอีกครั้ง และตรวจว่า `escalation_id` เหมือนเดิม
5. ตรวจว่า output มี `status: simulated-only`

### Checkpoint

- Tool คืน escalation ID เดิมเมื่อ input เดิม และไม่มี resource, file, message หรือ ticket ภายนอกถูกสร้าง

---

## Practice 2: ให้ Agent Framework agent เลือกเรียก tool

**Primary target:** สร้าง code-first Agent ที่เรียกใช้งาน `create_escalation` เมื่อ request ตรงเงื่อนไข

1. ใน `service_ops/escalation.py` ให้แทนที่ส่วนด้านล่างของ `TODO Exercise 6` ด้วย:

   ```python
   credential = credential_factory()
   client = client_factory(
       project_endpoint=settings.foundry_project_endpoint,
       model=settings.foundry_model,
       credential=credential,
   )
   return agent_factory(
       client=client,
       name="fabrikam-escalation-agent",
       instructions=(
           "Review synthetic service requests. Use create_escalation only when human review "
           "is required. Choose low, medium, or high priority. Always state that the result "
           "is simulated-only and never claim an external incident was created."
       ),
       tools=[create_escalation],
   )
   ```

2. เปิดไฟล์ [escalation-request.json](./files/escalation-request.json) แล้วคัดลอก `request_id`, `summary` และ `reason`
3. รัน:

   ```bash
   python -m service_ops agent --escalation --prompt "For synthetic request SR-2001, all users cannot sign in. Create a high-priority simulated escalation for human review."
   ```
   > **⚠️ Note:** หากเจอ error `FoundryChatClient` ที่ไม่รองรับ model รุ่นเก่า (เช่น gpt-4o) ให้ทำการ deploy model ตระกูล gpt ที่ใหม่กว่าเพิ่มเติมใน Foundry portal และแก้ค่า **FOUNDRY_MODEL** ใน `.env` ให้ตรงกับ model deployment


4. ตรวจว่า Agent เรียก tool และตอบด้วย `ESC-...`, `high` และ `simulated-only`
5. ทดสอบ request ที่ไม่ควร escalate:

   ```bash
   python -m service_ops agent --escalation --prompt "A learner asks where to find the weekly service report. Explain the next step without creating an escalation."
   ```

6. ตรวจว่าคำตอบที่สองไม่สร้าง escalation ID

### Checkpoint

- Agent เรียก tool เฉพาะกรณีของคำร้องที่ต้องให้คนตรวจ 

> **⚠️ Note:** Function tool เปรียบเหมือนแบบฟอร์มที่ Agent กรอกได้—ถ้าแบบฟอร์มนั้นกดส่งเข้าระบบจริง ต้องมี validation, authorization, audit และ human approval เพิ่มเติม Exercise นี้จึงใช้ simulation เท่านั้น

---

## Summary

เราเพิ่ม Agent Framework agent ที่เป็นเจ้าของ instructions และ local tool ใน code Exercise สุดท้ายจะจัด Agent สามบทบาทให้ทำงานต่อกันแบบ sequential orchestration
