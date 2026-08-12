# Optional extension: เผยแพร่ไปยัง Teams และ Microsoft 365 Copilot

กิจกรรมหลังชั้นเรียนนี้นำ portal-managed Fabrikam Agent จาก Exercise 4 ไปทดสอบในช่องทางที่องค์กรอนุมัติ โดยไม่สร้าง Agent หรือ knowledge source ซ้ำ

> **⚠️ ต้องตรวจสอบก่อนเริ่มอบรม:** Microsoft 365 entitlement, Microsoft 365 Copilot license, Foundry publishing availability, Azure Bot Service, custom app upload policy, app catalog policy, DLP, admin approval, network และ publish scope ต้องทดสอบด้วย ordinary learner account ใน tenant จริง กิจกรรมนี้อยู่นอก timed core และไม่ควรใช้เป็น checkpoint บังคับของเวลา 09:00–16:30

> **License:** Original workshop content © 2026 Amaround Co., Ltd. All rights reserved. Third-party notices are recorded in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

ใช้เวลาประมาณ **40 นาที** หลังผ่าน readiness gate

## Prerequisites

- Agent `fabrikam-service-operations-iq` ตอบพร้อม citation ใน Foundry Playground
- IT Admin ยืนยันว่า user นี้ publish หรือ upload custom Teams app ใน test scope ได้
- ถ้าทดสอบ Microsoft 365 Copilot ต้องมี license และ policy ที่รองรับ
- ผู้สอนให้ website, privacy policy, terms of use และ developer information ที่องค์กรอนุมัติ
- อ่าน [app-details.md](./files/app-details.md) และห้ามใส่ private URL หรือข้อมูลส่วนบุคคลลง public package

---

## Practice 1: เตรียม publishing package

**Primary target:** เตรียม metadata และ icons ที่ผ่านข้อกำหนดของ tenant โดยไม่ใส่ข้อมูลส่วนตัวหรือ URL สมมติ

1. เปิด [app-details.md](./files/app-details.md) แล้วใช้ชื่อกับคำอธิบายสังเคราะห์ที่เตรียมไว้
2. เปิด [color-icon.svg](./files/color-icon.svg) และ [outline-icon.svg](./files/outline-icon.svg) เพื่อตรวจ artwork ต้นฉบับ
3. Export ด้วยเครื่องมือกราฟิกที่องค์กรอนุมัติเป็น:
   - color icon: PNG ขนาด 192×192 pixels
   - outline icon: PNG ขนาด 32×32 pixels, เส้นสีขาวและพื้นหลังโปร่งใส
4. รับ website, privacy policy, terms และ developer information จาก IT Admin ห้ามใช้ private workspace path หรือ URL ที่ไม่ได้รับอนุมัติ
5. เก็บไฟล์ export ไว้เฉพาะใน working copy หรือช่องทางที่ผู้สอนกำหนด อย่า commit tenant-specific metadata

### Checkpoint

- มี PNG สองขนาดและ metadata ที่ IT Admin อนุมัติ โดยไม่มี credential, private URL หรือ personal contact

---

## Practice 2: Publish และทดสอบใน Microsoft Teams

**Primary target:** Publish Agent ไปยัง personal/shared test scope ที่ได้รับอนุมัติและตอบคำถาม grounded ใน Teams

1. เปิด Agent `fabrikam-service-operations-iq` ใน **Build > Agents**
2. เลือก **Publish > Publish to Teams and Microsoft 365 Copilot > Continue**
3. ใส่ app name, descriptions, developer information และ icons ที่ผ่าน Practice 1
4. เลือกเฉพาะ **Personal**, **Individual** หรือ **Shared test scope** ที่ IT Admin อนุมัติ คำเรียกอาจต่างกันตาม tenant
5. เลือก **Prepare Agent** แล้วรอ packaging เสร็จ
6. เลือก **Continue the in-product publishing flow** และ submit/publish ตาม scope ที่ได้รับอนุมัติ
7. ถ้า direct publish ไม่พร้อม แต่ custom app upload ได้ ให้ใช้ **Download & customize** แล้วส่ง package ผ่านเส้นทางที่ IT Admin กำหนด
8. ใน Microsoft Teams เปิด **Apps > Your agents** หรือบริเวณที่ tenant แสดง Agent แล้วถาม:

   ```text
   What is a Severity 1 service incident? Cite the source.
   ```

9. ตรวจว่าคำตอบสอดคล้องกับ `KB-SEVERITY-001`

### Checkpoint

- Agent เปิดใน Teams test scope และตอบคำถาม grounded หนึ่งครั้ง หรือบันทึก policy blocker โดยไม่ขยาย scope เอง

---

## Practice 3: ทดสอบ Microsoft 365 Copilot และ cleanup

**Primary target:** ยืนยัน Agent ใน Microsoft 365 Copilot เมื่อมี entitlement แล้วถอนการติดตั้งหรือส่งมอบ cleanup responsibility อย่างชัดเจน

1. ทำต่อเฉพาะเมื่อ IT Admin ยืนยัน Microsoft 365 Copilot license และ Agent publishing policy
2. เปิด Microsoft 365 Copilot แล้วหา Agent ใต้ **Your agents**, **Agents** หรือพื้นที่ที่ tenant แสดง
3. เลือก Agent แล้วถาม:

   ```text
   Which support channel should handle a duplicate charge? Cite the source.
   ```

4. ตรวจว่าคำตอบระบุ human billing specialist และอ้าง `KB-CHANNELS-002`
5. เมื่อทดสอบเสร็จ ให้ถอนการติดตั้ง app จาก Teams ตาม policy
6. ให้เจ้าของ resource ที่ผู้สอนระบุเป็นผู้ลบ published app, Azure Bot Service หรือ Agent ห้ามผู้เรียนลบ resource group ทั้งก้อนโดยไม่ได้รับอนุญาต

### Checkpoint

- Copilot test ผ่านพร้อม citation หรือระบุ entitlement/policy blocker ชัดเจน และมีชื่อผู้รับผิดชอบ cleanup โดยไม่ลบทรัพยากรเกินขอบเขต

> **💡 Fallback:** ถ้า tenant ไม่อนุญาต publishing ให้ผู้สอนสาธิตใน tenant ที่เตรียมไว้ ผู้เรียนส่งเฉพาะ readiness checklist กับ package metadata ไม่ควรขอ admin role เพิ่มเพื่อให้กิจกรรมผ่าน

---

## Summary

กิจกรรมเสริมนี้แสดงเส้นทางนำ Agent เดิมไปยัง Teams และ Microsoft 365 Copilot โดยถือ tenant policy, entitlement และ admin approval เป็นเงื่อนไขหลัก ไม่ใช่สิ่งที่ workshop รับประกันได้
