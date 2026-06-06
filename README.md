CloudNotesApp — אפליקציית פתקים ומשימות בטכנולוגיית Serverless ב-AWS

מערכת לניהול פתקים ומשימות המבוססת כולה על ארכיטקטורת Serverless בענן של AWS[cite: 2]. האפליקציה מאפשרת למשתמשים ליצור, לקרוא ולמחוק פתקים בזמן אמת באופן מאובטח, תוך הפרדה מלאה בין ה-Frontend ל-Backend לצורך השגת מהירות, שרידות וחיסכון במשאבים[cite: 2].

🔗 **קישור לאפליקציה החיה:** [cloudnotesapp.proj.rotem.click](https://cloudnotesapp.proj.rotem.click)[cite: 2]  
👥 **מפתחים:** נועם אופק ונועה גיבלי[cite: 2]  
🏫 **מוסד אקדמי:** המכללה האקדמית עמק יזרעאל[cite: 2]  

---

## 🏗️ ארכיטקטורת המערכת

המערכת בנויה על טהרת ה-Serverless[cite: 2]. כל הרכיבים גדלים ומצטמצמים באופן אוטומטי (Auto-scaling) בהתאם לעומס, ללא צורך בניהול או תחזוקת שרתים[cite: 2].

[ דפדפן המשתמש ]
│
▼ (HTTPS / דומיין מותאם אישית)
[ Amazon Route 53 ] ──► [ AWS Certificate Manager (ACM) ]
│
▼
[ Amazon CloudFront (CDN) ]
├── 📄 קבצי אתר סטטיים ──► [ Amazon S3 Frontend Bucket ]
└── ⚡ בקשות API        ──► [ Amazon API Gateway (REST) ] ──► [ AWS Lambda ] ──► [ Amazon DynamoDB ]
│
▼
[ Amazon CloudWatch Logs ]


### זרימת הבקשות במערכת:
1. **רשת ואבטחה:** המשתמש גולש לדומיין המותאם אישית המנוהל ב-**Amazon Route 53**[cite: 2]. התעבורה מאובטחת בפרוטוקול HTTPS באמצעות תעודת אבטחה של **AWS Certificate Manager (ACM)**[cite: 2].
2. **הגשת קבצים (Edge):** שירות **Amazon CloudFront** מפיץ ומבצע מטמון (Cache) לקבצי ה-Frontend הסטטיים שנמצאים בתוך באקט **Amazon S3**[cite: 2].
3. **ניתוב בקשות API:** בקשות דינמיות (תחת הנתיב `/notes`) מנותבות דרך **Amazon API Gateway** בחיבור REST API Proxy[cite: 2].
4. **לוגיקה ומחשוב:** ה-API Gateway מפעיל פונקציית **AWS Lambda** הרצה על סביבת **Python 3.12** שמבצעת את הלוגיקה העסקית[cite: 2].
5. **בסיס נתונים:** פונקציית הלמדא קוראת וכותבת את נתוני הפתקים אל טבלת **Amazon DynamoDB** (בסיס נתונים NoSQL)[cite: 2].
6. **ניטור ומעקב:** כל הלוגים וביצועי המערכת נשמרים ומנוטרים בזמן אמת ב-**Amazon CloudWatch**[cite: 2].

---

## 📁 מבנה תיקיות הפרויקט

cloud-notes-app/
├── .github/workflows/
│   └── deploy-frontend.yml      # קובץ האוטומציה של צינור ה-CI/CD
├── backend/                     # קוד המקור של פונקציית הלמדא (Python)
├── frontend/                    # קבצי האתר הסטטיים (HTML, CSS, JS)
└── README.md                    # קובץ תיעוד זה


---

## 🛠️ פירוט רכיבי ה-AWS בפרויקט

### 💾 אחסון והפצה (Amazon S3 & CloudFront)
* **באקט ה-S3:** קבצי האתר הסטטיים מאוחסנים בבאקט ייעודי בשם `cloud-notes-frontend-noam-team`[cite: 2].
* **הפצת CDN:** שירות CloudFront מוגדר להפצת הקבצים דרך דומיין מותאם אישית, ומפנה אוטומטית לקובץ המקור `index.html`[cite: 2].

### 🔌 שכבת ה-API (Amazon API Gateway)
* **סוג ה-API:** מסוג REST API המנהל את ה-Resource עבור הנתיב `/notes`[cite: 2].
* **אסטרטגיית ניתוב:** שימוש במתודת `ANY` ו-`OPTIONS` המעבירה את כל הבקשות והפרוטוקולים ישירות לפונקציית ה-Lambda (Proxy Integration)[cite: 2].

### ⚡ שכבת המחשוב (AWS Lambda)
* **סביבת ריצה:** Python 3.12[cite: 2].
* **ביצועים בשטח:** בדיקות הניטור מראות על זמן ריצה מהיר של כ-**254.04 מילישניות** לביצוע פעולה מלאה מול בסיס הנתונים[cite: 2].

### 📊 בסיס הנתונים (Amazon DynamoDB)
הנתונים נשמרים בטבלה מנוהלת בשם `cloud-notes-table` הפועלת במודל On-Demand (משאבים ותמחור לפי שימוש בפועל)[cite: 2].

| שם השדה | סוג הנתון | תפקיד | תיאור |
| :--- | :--- | :--- | :--- |
| `taskId` | `String` | **Partition Key (PK)** | מזהה ייחודי שנוצר עבור כל פתק במערכת[cite: 2]. |
| `id` | `String` | Attribute | מזהה פנימי תואם[cite: 2]. |
| `title` | `String` | Attribute | כותרת הפתק שהמשתמש הזין[cite: 2]. |
| `content` | `String` | Attribute | תוכן הפתק שהמשתמש הזין[cite: 2]. |

---

## 🔐 אבטחה וניהול הרשאות (IAM)

הפרויקט מיישם את עקרון ההרשאות המינימליות (Least Privilege) ואינו מכיל סיסמאות או מפתחות קשיחים בקוד[cite: 1, 2]:

1. **חיבור מאובטח ל-GitHub Actions (OIDC):**
   * זיהוי הצינור מול AWS מתבצע ללא שימוש במפתחות קשיחים (AWS Access Keys) בהגדרות הרפוזיטורי[cite: 2].
   * במקום זאת, מוגדר רול ייעודי המשתמש ב-OpenID Connect (OIDC) כדי לאפשר לגיטהאב לבצע אימות זמני ומאובטח מול AWS[cite: 2].
   * יחסי האמון (Trust Boundary) מוגדרים כך שרק הרפוזיטורי הספציפי שלכם מורשה להשתמש ברול זה: `repo:YVC-CloudDev/cloud-notes-app:*`[cite: 2].
2. **הרשאות פונקציית הלמדא:**
   * הפונקציה משתמשת ברול ייעודי קשיח (`cloud-notes-backend-role-rwkfszjp`)[cite: 2].
   * הרול מעניק לה אך ורק את ההרשאות הנדרשות לפעילותה: כתיבה וקריאה מטבלת הדינמו (`AmazonDynamoDBFullAccess`) וכתיבת לוגים ל-CloudWatch (`AWSLambdaBasicExecutionRole`)[cite: 2].

---

## 🚀 צינור אוטומציה ופריסה (CI/CD)

הפרויקט כולל צינור פריסה אוטומטי מלא המבוסס על **GitHub Actions**[cite: 2]:

* **טריגר להפעלה:** הצינור מופעל אוטומטית בכל ביצוע `push` או מיזוג (Merge) של קוד לענף ה-`main`[cite: 2].
* **שלבי הריצה המרכזיים:**
  1. משיכת קוד המקור המעודכן מהרפוזיטורי[cite: 2].
  2. ביצוע אימות מאובטח וקבלת הרשאות זמניות מול AWS באמצעות מנגנון ה-OIDC[cite: 2].
  3. העלאת קבצי ה-Frontend המעודכנים ישירות לבאקט ה-S3[cite: 2].
  4. הרצת פקודת **CloudFront Invalidation** אוטומטית כדי לנקות את ה-Cache ולרענן את האתר אצל המשתמשים באופן מיידי[cite: 2].
* **זמן ריצה:** תהליך הפריסה והעדכון האוטומטי לוקח כ-**15 שניות** בלבד[cite: 2].

### 🔒 משתני סוד (Secrets) הנדרשים ברפוזיטורי:
* `AWS_REGION` — אזור הענן בו מותקנת התשתית (`eu-north-1`)[cite: 2].
* `AWS_ROLE_TO_ASSUME` — מזהה ה-ARN של ה-IAM Role לצורך הפריסה האוטומטית[cite: 2].
* `CLOUDFRONT_DISTRIBUTION_ID` — מזהה הפצת ה-CloudFront לצורך ניקוי ה-Cache[cite: 2].
* `FRONTEND_BUCKET_NAME` — שם באקט ה-S3 אליו מועלים קבצי הסטטיק[cite: 2].
