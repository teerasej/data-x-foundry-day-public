# Exercise 6: สร้าง code-first Agent Framework agent

Fabrikam ต้องการให้ Agent เสนอ escalation ได้ แต่ต้องไม่สร้าง incident จริงระหว่างเรียน เราจะสร้าง local function tool ที่ให้ผลลัพธ์ซ้ำได้และระบุ `simulated-only` แล้วเชื่อมกับ `FoundryChatClient`

> **License:** Original workshop content © 2026 Amaround Co., Ltd. All rights reserved. Third-party notices are recorded in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

ใช้เวลาประมาณ **30 นาที** และใช้ codebase, Foundry project, model และ Azure CLI sign-in เดิม

## Prerequisites

- ทำ Exercise 2 เสร็จและเข้าใจรูปแบบ `Agent(client=..., tools=[...])`
- มีไฟล์ [escalation-request.json](./files/escalation-request.json)
- ยืนยันว่า Exercise นี้ไม่เชื่อมต่อ ticketing, email, Teams หรือ production API

---

## Practice 1: ตรวจ simulated escalation tool

**Primary target:** เรียกเครื่องมือ escalation แบบ deterministic และตรวจว่าไม่มี external side effect

1. เปิด `service_ops/escalation.py` แล้วอ่าน `create_escalation()`
2. สังเกตว่า ID สร้างจากค่าของ request ด้วย SHA-256 ไม่ใช่การเรียก API ภายนอก
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

**Primary target:** สร้าง code-first Agent ที่เรียก `create_escalation` เมื่อ request ตรงเงื่อนไขและอธิบายว่าเป็น simulation

1. ใน `service_ops/escalation.py` แทนส่วน `TODO Exercise 6` ด้วย:

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

2. เปิด [escalation-request.json](./files/escalation-request.json) แล้วคัดลอก `request_id`, `summary` และ `reason`
3. รัน:

   ```bash
   python -m service_ops agent --escalation --prompt "For synthetic request SR-2001, all users cannot sign in. Create a high-priority simulated escalation for human review."
   ```

4. ตรวจว่า Agent เรียก tool และตอบด้วย `ESC-...`, `high` และ `simulated-only`
5. ทดสอบ request ที่ไม่ควร escalate:

   ```bash
   python -m service_ops agent --escalation --prompt "A learner asks where to find the weekly service report. Explain the next step without creating an escalation."
   ```

6. ตรวจว่าคำตอบที่สองไม่สร้าง escalation ID

### Checkpoint

- Agent เรียก tool เฉพาะกรณีที่ต้องให้คนตรวจ และไม่อ้างว่าได้สร้าง incident จริง

> **⚠️ Note:** Function tool เปรียบเหมือนแบบฟอร์มที่ Agent กรอกได้—ถ้าแบบฟอร์มนั้นกดส่งเข้าระบบจริง ต้องมี validation, authorization, audit และ human approval เพิ่มเติม Exercise นี้จึงใช้ simulation เท่านั้น

---

## Summary

เราเพิ่ม Agent Framework agent ที่เป็นเจ้าของ instructions และ local tool ใน code Exercise สุดท้ายจะจัด Agent สามบทบาทให้ทำงานต่อกันแบบ sequential orchestration
