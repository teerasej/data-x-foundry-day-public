# Exercise 3: เชื่อมต่อ Agent กับ MCP

Fabrikam ต้องการให้ Agent ใช้ข้อมูลนอก prompt ได้อย่างควบคุม ใน Exercise นี้เราจะเชื่อมต่อ Microsoft Learn MCP สำหรับเอกสาร Microsoft และสร้าง local MCP server ที่ให้บริการสถานะระบบจากข้อมูลสังเคราะห์

> **License:** Original workshop content © 2026 Amaround Co., Ltd. All rights reserved. Third-party notices are recorded in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

ใช้เวลาประมาณ **60 นาที** และใช้ Foundry project, model deployment, `.venv` และ `.env` เดิมจาก Exercise 1–2

## Prerequisites

- `python -m service_ops check` ไม่มีสถานะ `ERROR`
- `az login --use-device-code` สำเร็จ และบัญชีอยู่ใน resource group ที่ได้รับมอบหมาย
- ทำ `service_ops/agent.py` จาก Exercise 2 เสร็จแล้ว
- ตรวจไฟล์ [service-status.json](./files/service-status.json) และยืนยันว่าเป็นข้อมูลสังเคราะห์
- Network อนุญาต `https://learn.microsoft.com/api/mcp`; ถ้าถูกบล็อกให้ใช้ local MCP ใน Practice 2–3

> **⚠️ Note:** MCP เปรียบเหมือนปลั๊กพ่วงมาตรฐานที่ทำให้ Agent ต่อกับเครื่องมือหลายชนิดได้ แต่เรายังต้องเลือกแหล่งที่เชื่อถือได้และจำกัดข้อมูลที่ส่งออก ห้ามส่ง credential, production data หรือข้อมูลลูกค้าไปยัง MCP server

---

## Practice 1: ใช้ Microsoft Learn MCP

**Primary target:** เชื่อม `FoundryChatClient` กับ Microsoft Learn MCP และให้ Agent ตอบจากเอกสาร Microsoft ปัจจุบัน

1. เปิด `service_ops/mcp_agent.py` แล้วสังเกต endpoint ที่กำหนดไว้เป็น `https://learn.microsoft.com/api/mcp`
2. ในฟังก์ชัน `build_mcp_agent()` ให้แทนส่วน `TODO Exercise 3` ด้วยโค้ดนี้:

   ```python
   endpoint = (
       MICROSOFT_LEARN_MCP_ENDPOINT
       if source == "learn"
       else settings.local_mcp_endpoint
   )
   credential = credential_factory()
   client = client_factory(
       project_endpoint=settings.foundry_project_endpoint,
       model=settings.foundry_model,
       credential=credential,
   )
   mcp_tool = tool_factory(
       name=f"{source}-mcp",
       url=endpoint,
       approval_mode="never_require",
   )
   return agent_factory(
       client=client,
       name="fabrikam-mcp-agent",
       instructions=MCP_AGENT_INSTRUCTIONS,
       tools=mcp_tool,
   )
   ```

   ใน workshop นี้เราใช้ `never_require` เฉพาะ endpoint ที่ผู้สอนตรวจแล้วและ prompt ที่ผู้เรียนเป็นผู้เริ่มเอง ระบบ production ควรประเมิน approval และ allow-list ตามความเสี่ยง

3. บันทึกไฟล์ แล้วรัน:

   ```bash
   python -m service_ops mcp-agent --source learn --prompt "จาก Microsoft Learn อธิบายว่า Streamable HTTP ใช้กับ MCP อย่างไร พร้อมบอกชื่อแหล่งข้อมูล"
   ```

4. สังเกตว่าคำตอบกล่าวถึง Microsoft Learn หรือ MCP tool และไม่อ้างว่าข้อมูลสังเคราะห์เป็นข้อมูลจริง

### Checkpoint

- Agent ตอบคำถามจาก Microsoft Learn MCP ได้หนึ่งครั้ง หรือบันทึกว่า network บล็อก endpoint แล้วไปใช้ local MCP fallback

---

## Practice 2: สร้าง local service-status MCP server

**Primary target:** เปิดเผยฟังก์ชันอ่านสถานะสังเคราะห์เป็น MCP tools ผ่าน Streamable HTTP ที่ port 8000

1. เปิด `service_ops/mcp_server.py` แล้วตรวจว่า `find_service_status()` และ `summarize_queue()` อ่านเฉพาะไฟล์ของ Exercise นี้
2. แทนส่วน `TODO Exercise 3` ใน `create_mcp_server()` ด้วยโค้ดนี้:

   ```python
   server = MCPServer(
       name="fabrikam-service-status",
       instructions="Return synthetic training data only.",
   )

   @server.tool()
   def get_service_status(service_name: str) -> dict[str, Any]:
       """Return one synthetic service status by name."""
       return find_service_status(service_name)

   @server.tool()
   def get_queue_summary() -> dict[str, Any]:
       """Return the synthetic support queue summary."""
       return summarize_queue()

   return server
   ```

3. บันทึกไฟล์ เปิด Terminal แรก แล้วรัน:

   ```bash
   python -m service_ops mcp-server
   ```

4. รอจน server ทำงานที่ `http://127.0.0.1:8000/mcp` และ Codespaces แสดง forwarded port 8000

### Checkpoint

- Terminal แรกยังรัน local MCP server อยู่ และ endpoint คือ `/mcp` ผ่าน Streamable HTTP

---

## Practice 3: ให้ Agent เรียก local MCP tools

**Primary target:** ให้ MCP-enabled Agent เรียกเครื่องมือสถานะบริการและสรุปผลโดยระบุว่าเป็นข้อมูลสังเคราะห์

1. เปิด Terminal ที่สอง โดยไม่หยุด server ใน Terminal แรก
2. ตรวจ `.env` ว่ามีค่า:

   ```text
   LOCAL_MCP_ENDPOINT=http://127.0.0.1:8000/mcp
   ```

3. รันคำถามที่บังคับให้ Agent ใช้ทั้งสอง tools:

   ```bash
   python -m service_ops mcp-agent --source local --prompt "ตรวจสถานะ Customer Portal และสรุปคิวงานปัจจุบัน ระบุชัดเจนว่าเป็น synthetic training data"
   ```

4. ตรวจคำตอบว่ามี `degraded`, จำนวนคำขอที่รอ `14` และคำเตือนว่าไม่ใช่ production data
5. กลับไป Terminal แรก แล้วกด **Ctrl+C** เพื่อหยุด server เมื่อทดสอบเสร็จ

### Checkpoint

- Agent เรียก local MCP tools สำเร็จและตอบด้วยค่าจาก `service-status.json` โดยไม่สร้างข้อมูลเพิ่มเอง

> **💡 Fallback:** ถ้า Microsoft Learn MCP ถูก network บล็อก ให้ใช้ผลจาก Practice 3 เป็น checkpoint หลัก และให้ผู้สอนสาธิต remote endpoint จาก environment ที่อนุญาต

---

## Summary

เราเพิ่มทั้ง remote และ local MCP ให้ Agent โดยใช้ codebase และ Foundry project เดิม Exercise ถัดไปจะเปลี่ยนจากข้อมูล snapshot เป็นความรู้ที่ค้นคืนได้พร้อม citation ด้วย Foundry IQ
