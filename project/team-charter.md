# Team Charter & Working Agreement

## 1. สมาชิกและบทบาท
| ชื่อ | GitHub Username | บทบาท |
|---|---|---|
| นายอมรเทพ ยมภา | amonthep-kong | Product Owner |
| นางสาวหทัยรัตน์ ใจธรรม | hathairatja-wq | Scrum Master / Developer |
| นางสาวกุลปรียา ประดิษฐ์ | kulpreeya-a11y | Developer |

## 2. Branching Strategy & Code Review
* **ใช้ GitHub Flow:** 
  * Main branch ต้อง deploy ได้เสมอ ห้าม commit โดยตรง
  * ทุก feature ใหม่ต้องสร้าง branch ชื่อ `feat/<issue-number>-<short-name>`
  * ทุก PR ต้องผ่านการ review ก่อน merge
* **กติกาการ Review:** สมาชิกในทีมอย่างน้อย 1 คนต้อง review และ approve และ **คนที่กด merge ต้องไม่ใช่เจ้าของ PR** เพื่อความโปร่งใสและช่วยกันตรวจสอบคุณภาพโค้ด

## 3. WIP limit
* คอลัมน์ In Progress มีการ์ดพร้อมกันได้ไม่เกิน 3 ใบ (ตามจำนวนสมาชิกในทีม)
* เมื่อการ์ดเต็ม WIP limit ห้ามลากการ์ดใหม่เข้ามา ให้ทำคอร์สงานเดิมให้เสร็จ หรือช่วยกัน review PR ที่ค้างอยู่ใน In Review ก่อน

## 4. Sprint Goal (Sprint 1)
* ส่งมอบโครงสร้างพื้นฐานระบบ RAG Assistant และฟังก์ชันการค้นหาเอกสารพื้นฐานที่ผ่านเกณฑ์ Acceptance Criteria ครบถ้วน

## 5. AI Usage Policy
* ใช้ AI (เช่น Gemini, Claude Code, GitHub Copilot) ช่วยเขียน draft code, unit test และ draft commit message ได้
* ทุก commit message ที่ AI generate ต้องอ่านและตรวจสอบให้ตรงกับ diff จริงก่อน commit ทุกครั้ง
* ห้าม copy code จาก AI โดยไม่อ่านและทำความเข้าใจก่อน
* ใช้เฉพาะ AI ที่ไม่มีค่าใช้จ่ายหรือช่องทางที่รายวิชาอนุญาต