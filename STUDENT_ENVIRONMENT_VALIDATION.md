# ตรวจความพร้อมของบัญชีและเครื่องก่อนเริ่ม Workshop

เอกสารนี้ช่วยให้ผู้เรียนตรวจว่า GitHub, Codespaces, Azure account, Resource group และ Microsoft Foundry พร้อมใช้งานก่อนเริ่ม Exercise ให้ลองทำตามลำดับและหยุดแจ้งทีม Support ทันทีเมื่อผลลัพธ์ไม่ตรงกับ Checkpoint

> **License และค่าใช้จ่าย:** GitHub Codespaces มี included usage และค่าใช้จ่ายต่างกันตามประเภทบัญชี ส่วน Azure และ Microsoft Foundry อาจมีค่าใช้จ่ายตามการใช้งาน ให้ใช้เฉพาะบัญชี, Resource group, Region และ Model ที่ผู้จัดอบรมกำหนด

## เตรียมข้อมูลก่อนตรวจ

ขอข้อมูลต่อไปนี้จาก IT Admin หรือผู้สอน โดยไม่บันทึกรหัสผ่านหรือข้อมูลลับลงใน Repository:

- Azure account ที่ใช้ใน Workshop
- ชื่อ Resource group ที่ได้รับมอบหมาย
- Subscription, Region และ Model ที่อนุมัติให้ใช้
- GitHub account ที่ต้องใช้: Personal account หรือ Organization account
- Branch ที่ผู้สอนกำหนดให้เปิด Codespace
- ช่องทางติดต่อทีม Support

Azure account และ GitHub account อาจใช้อีเมลคนละชื่อกันได้ ให้ตรวจแต่ละบัญชีแยกกัน

---

## Practice 1: ตรวจ GitHub account และ Repository

**Primary target:** ยืนยันว่า GitHub account เปิด Workshop repository และเห็นตัวเลือกสร้าง Codespace ได้

1. เปิด GitHub ใน InPrivate/Incognito window แล้ว Sign in ด้วยบัญชีที่ผู้จัดอบรมกำหนด
2. เปิด Workshop repository จาก Link ที่ผู้สอนให้
3. ตรวจว่าเห็น `README.md` และโฟลเดอร์ `exercises`
4. เลือก **Code** แล้วเปิด Tab **Codespaces**
5. ตรวจว่าเห็น **Create codespace on current branch** หรือชื่อ Branch ที่ผู้สอนกำหนด
6. ถ้าใช้ Organization account ให้ตรวจว่าบัญชีอยู่ใน Organization หรือได้รับสิทธิ์ Collaborator ตามที่ IT แจ้ง

> **⚠️ Note:** อย่ากดสร้าง Codespace ซ้ำหลายตัว เพราะอาจใช้ Compute และ Storage quota เพิ่ม หากไม่เห็น Tab **Codespaces** ให้หยุดและแจ้งทีม Support พร้อมระบุเพียงว่าบัญชีเป็น Personal, Organization-managed หรือ Enterprise Managed User

### Checkpoint: GitHub และ Repository

- เปิด Workshop repository ได้
- เห็น `README.md` และ `exercises`
- เห็นตัวเลือกสร้าง Codespace จาก Branch ที่กำหนด

---

## Practice 2: เปิด Codespace และตรวจเครื่องมือ

**Primary target:** เปิด Development environment และยืนยันว่าเครื่องมือพื้นฐานของ Workshop พร้อมใช้งาน

1. เลือก **Code > Codespaces > Create codespace on current branch**
2. รอจน Codespace เปิดและ `postCreateCommand` ติดตั้ง Dependencies เสร็จ
3. เปิด **Terminal** แล้วรัน:

   ```bash
   python -m service_ops check
   ```

4. ตรวจว่ารายการต่อไปนี้แสดง `READY`:

   - Python 3.12
   - Repository virtual environment `.venv`
   - Git
   - Azure CLI
   - Python imports ที่ Workshop ต้องใช้

5. หาก `Azure sign-in` หรือ `.env configuration` แสดง `ACTION` ก่อนทำ Exercise 1 ให้ทำ Practice ถัดไป นี่เป็นผลที่คาดไว้

### Checkpoint: Codespace และเครื่องมือ

- Codespace เปิดสำเร็จ
- Bootstrap ทำงานจบโดยไม่มี `ERROR`
- Base tools และ Python imports แสดง `READY`

> **💡 Tip:** ถ้า Codespaces ใช้ไม่ได้ ให้ใช้ VS Code พร้อม Dev Containers ตามที่ IT Admin เตรียมไว้ แล้วเปิด Repository ด้วย **Dev Containers: Reopen in Container** อย่าติดตั้ง Dependencies แบบเดาเองบนเครื่อง

---

## Practice 3: ลงชื่อเข้าใช้ Azure และตรวจ Resource group

**Primary target:** ยืนยันว่า Azure account เข้าได้และมองเห็น Resource group ที่ได้รับมอบหมาย

1. ใน Codespace Terminal รัน:

   ```bash
   az login --use-device-code
   ```

2. เปิดหน้า Sign in ที่คำสั่งแสดง แล้วกรอก Device Code ด้วย Azure account ที่ IT Admin จัดเตรียม
3. ทำ MFA หรือ Conditional Access ตามนโยบายขององค์กร
4. ห้ามส่ง Device Code, Password หรือ Sign-in Link ให้บุคคลอื่น
5. ตรวจชื่อ Account โดยไม่แสดง Tenant ID หรือ Subscription ID:

   ```bash
   az account show --query "{account:name,user:user.name}" --output table
   ```

6. แทน `<assigned-resource-group>` ด้วยชื่อที่ IT Admin แจ้ง แล้วรัน:

   ```bash
   az group show \
     --name <assigned-resource-group> \
     --query "{name:name,location:location}" \
     --output table
   ```

7. ตรวจว่าชื่อ Resource group ตรงกับที่ได้รับมอบหมายทุกตัวอักษร

### Checkpoint: Azure account และ Resource group

- `az login --use-device-code` สำเร็จ
- Account name และ Username ตรงกับข้อมูลจาก IT
- `az group show` แสดง Resource group ที่ได้รับมอบหมาย

> **⚠️ Note:** หาก Login สำเร็จแต่เข้าถึง Resource group ไม่ได้ ให้รอการกระจาย RBAC แล้ว Sign out/Sign in ใหม่ ห้ามเปลี่ยนไปใช้ Resource group อื่นเอง

---

## Practice 4: ตรวจ Azure RBAC ทั้งแปดรายการ

**Primary target:** ยืนยันว่า Azure account มี Role ที่ Workshop ต้องใช้ครบใน Resource group ของตน

1. เปิด [Azure portal](https://portal.azure.com) แล้ว Sign in ด้วย Azure account เดียวกับ Azure CLI
2. เปิด **Resource groups** แล้วเลือก Resource group ที่ได้รับมอบหมาย
3. เลือก **Access control (IAM) > View my access**
4. ตรวจว่าพบ Assignment ต่อไปนี้ครบแปดรายการที่ Resource group นี้:

   1. `Contributor`
   2. `Foundry Project Manager`
   3. `Cognitive Services User`
   4. `Storage Blob Data Contributor`
   5. `Search Service Contributor`
   6. `Search Index Data Contributor`
   7. `Search Index Data Reader`
   8. `Role Based Access Control Administrator` แบบมี Condition ที่ IT กำหนด

5. ตรวจว่า Scope ของ Assignment คือ Resource group ที่ได้รับ ไม่ใช่ Subscription
6. ผู้เรียนไม่ต้องเปิดหรือแก้ไข Condition ของ `Role Based Access Control Administrator` เพราะ IT Admin เป็นผู้ยืนยันว่า Condition ป้องกันการมอบ `Owner`, `User Access Administrator` และ `Role Based Access Control Administrator`

`Cognitive Services User` ช่วยให้บัญชีผู้เรียนเรียก Model endpoint ด้วย Microsoft Entra authentication ส่วน `Foundry Project Manager` ใช้สร้างและจัดการ Project, Agent และ Workflow จึงต้องมีทั้งสอง Role

Role ของผู้เรียนไม่ได้แทน Role ของ Managed identity ตัวอย่างเช่น Agent ที่ทำงานด้วย Managed identity ยังต้องมี `Search Index Data Reader` ของตัวเองเพื่ออ่าน Knowledge base

### Checkpoint: Azure RBAC

- เห็น Assignment ครบทั้งแปดรายการ
- ทุก Assignment อยู่ใน Resource group ที่ถูกต้อง
- ไม่พบ Role ที่ Subscription scope ซึ่ง IT ไม่ได้แจ้งไว้

---

## Practice 5: ตรวจ Microsoft Foundry portal

**Primary target:** ยืนยันว่า Azure account เปิด Microsoft Foundry และเลือก Environment ที่ได้รับได้โดยไม่สร้าง Resource ผิด Scope

1. เปิด [Microsoft Foundry](https://ai.azure.com) แล้ว Sign in ด้วย Azure account เดียวกับ Practice 3
2. เปิดหน้าสร้างหรือเลือก Project ตามประสบการณ์ **New Foundry** ที่ผู้สอนกำหนด
3. ตรวจว่า Subscription ที่ IT Admin แจ้งปรากฏในรายการ
4. ตรวจว่าเลือก Resource group ที่ได้รับมอบหมายได้
5. ตรวจว่า Region ที่ผู้สอนกำหนดปรากฏและ Model ที่จะใช้ได้รับการยืนยันแล้ว
6. หยุดก่อนกด **Create** หากยังไม่เริ่ม Exercise 1

### Checkpoint: Microsoft Foundry

- เปิด Microsoft Foundry portal ได้
- เลือก Subscription และ Resource group ที่ได้รับมอบหมายได้
- ไม่เลือก Resource group ของผู้เรียนคนอื่นหรือ Region/Model ที่ไม่ได้รับอนุมัติ

---

## Practice 6: ตรวจ Network และบริการภายนอก

**Primary target:** ยืนยันว่าเครือข่าย Workshop เข้าถึงบริการที่ Exercise ต้องใช้ได้

1. จาก Browser เดียวกับที่ใช้ Workshop ตรวจว่าเปิดได้:

   - GitHub repository
   - GitHub Codespaces
   - Azure portal
   - Microsoft Foundry portal
   - [Microsoft Learn](https://learn.microsoft.com)

2. ใน Codespace รัน Readiness check อีกครั้ง:

   ```bash
   python -m service_ops check
   ```

3. ตรวจว่า Azure sign-in เปลี่ยนเป็น `READY`
4. ถ้า `.env configuration` ยังเป็น `ACTION` ก่อน Exercise 1 ถือว่าเป็นผลที่คาดไว้
5. หากพบ `EACCES`, `ECONNREFUSED`, `ENOTFOUND`, Certificate error หรือ Codespace ตัดการเชื่อมต่อ ให้ส่งเฉพาะ Error message ที่ไม่มี Token หรือ ID ให้ทีม Support

### Checkpoint: Network

- Browser เปิด GitHub, Azure และ Microsoft Foundry ได้
- Codespace เชื่อมต่อได้ต่อเนื่อง
- Azure sign-in แสดง `READY`

---

## Final readiness checkpoint

ก่อนเริ่ม Exercise 1 ให้ยืนยันครบทุกข้อ:

- [ ] GitHub account เปิด Repository และ Codespace ได้
- [ ] Codespace หรือ Dev Container fallback แสดง Base tools เป็น `READY`
- [ ] Azure CLI Sign in สำเร็จ
- [ ] เข้าถึง Resource group ที่ได้รับมอบหมายได้
- [ ] เห็น Azure Assignment ครบทั้งแปดรายการ
- [ ] Microsoft Foundry เปิดและเลือก Resource group ที่ได้รับได้
- [ ] ไม่ได้บันทึก Password, Device Code, Token, Tenant ID หรือ Subscription ID ลงใน Repository หรือ Screenshot

หาก Workshop ยังไม่เริ่มทันที ให้หยุด Codespace เพื่อลด Compute usage โดยเปิด [Your Codespaces](https://github.com/codespaces) แล้วเลือก **Stop codespace**

## Summary

เราได้ตรวจ GitHub, Codespaces, Azure CLI, Azure RBAC, Resource group และ Microsoft Foundry แล้ว ขั้นต่อไปให้กลับไปที่ [Workshop README](./README.md) และเริ่ม Exercise 1 ตามคำแนะนำของผู้สอน
