# CloudNotesApp - אפליקציית ניהול פתקים ומשימות בענן

אפליקציית פתקים ומשימות מבוססת ארכיטקטורת **Serverless** מלאה על גבי תשתית **AWS**. המערכת מאפשרת למשתמשים ליצור משימות, לצפות בהן בזמן אמת ולמחוק אותן בצורה מאובטחת ומהירה, תוך ניצול מקסימלי של יתרונות הענן: סקילביליות, זמינות גבוהה ועלויות אפסיות בזמן מנוחה (Pay-as-you-go).

## קישורים מהירים

* **לינק לאפליקציה החיה:** [https://cloudnotesapp.proj.rotem.click](https://cloudnotesapp.proj.rotem.click)
* **מאגר הקוד (GitHub Repository):** `https://github.com/YVC-CloudDev/cloud-notes-app`

---

## ארכיטקטורת המערכת והשירותים (Tech Stack)

המערכת בנויה ומנוהלת כולה בתוך תשתית AWS ומחולקת לשכבות הבאות:

### Frontend (חווית משתמש)
* **Amazon S3:** מארח את קבצי האתר הסטטיים (HTML, CSS, JavaScript) בצורה מאובטחת ויציבה.
* **Amazon CloudFront (CDN):** מפיץ את האתר ברחבי העולם באמצעות שרתי קצה (Edge Locations) לטעינה מהירה, ומנהל את החיבור המאובטח בפרוטוקול HTTPS.

### Backend (לוגיקה ו-API)
* **Amazon API Gateway:** חושף ומנהל את נקודות הקצה (REST API HTTP Endpoints) של השרת. משתמש ב-**Lambda Proxy Integration** לניהול מלא של בקשות הלקוח ומאפשר מדיניות CORS מורחבת.
* **AWS Lambda (Python 3.12):** פונקציות סרברלס שמבצעות את הלוגיקה העסקית. הפונקציה מזהה את מתודת ה-HTTP ומטפלת בבקשות: `GET` (שליפת פתקים), `POST` (הוספת פתק חדש) ו-`DELETE` (מחיקת פתק לפי מזהה ייחודי).

### Database & Security (נתונים ואבטחה)
* **Amazon DynamoDB:** בסיס נתונים NoSQL מהיר המאחסן את הפתקים בטבלה ייעודית (`cloud-notes-table`) באמצעות מפתח ראשי (`taskId`).
* **AWS IAM (Identity and Access Management):** ניהול הרשאות מאובטח. פונקציית הלמדא משתמשת ב-Execution Role פנימי בעל הרשאות גישה ל-DynamoDB בלבד, **ללא שמירה של מפתחות אבטחה (Access Keys) או סודות בקוד האפליקציה**.
* **AWS Certificate Manager (ACM):** הנפקת תעודת SSL/TLS מותאמת אישית לניהול הצפנה ואבטחת האתר באמצעות HTTPS.
* **Amazon Route 53:** ניהול רשומות ה-DNS וניתוב הדומיין המכללתי (`proj.rotem.click`) ישירות אל ה-CloudFront באמצעות רשומות מסוג Alias.

### Monitoring (ניטור ותקינות)
* **Amazon CloudWatch:** איסוף לוגים ומטריקות (Logs & Metrics) בזמן אמת מתוך ריצות פונקציית הלמדא, המאפשרים איתור תקלות וניתוח ביצועים של השרת.

---

## 🗺️ תרשים ארכיטקטורה (Architecture Diagram)
