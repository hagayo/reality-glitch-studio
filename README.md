# Reality Glitch Studio

אפליקציית Streamlit יצירתית שמאפשרת להעלות תמונה, לבנות Pipeline של אפקטים,
להשתמש ב-Presets מוכנים ולהוריד את התוצאה כתמונת PNG או כ-GIF מונפש.

הפרויקט נבנה כדוגמה לימודית מקצועית לפיתוח Python מודולרי באמצעות UV,
Streamlit, Pillow ו-NumPy, תוך יישום עקרונות SOLID, Dependency Injection,
בדיקות אוטומטיות ו-CI באמצעות GitHub Actions.

## יכולות מרכזיות

- Pipeline של עד ארבעה אפקטים לפי סדר בחירת המשתמש
- תצוגת תוצאת ביניים לאחר כל שלב
- Presets מוכנים לסגנונות חזותיים שונים
- יצירת PNG ללא קובץ זמני
- יצירת GIF מונפש בתנועת Ping-Pong
- אפקטים עצמאיים הרשומים ב-Registry
- ממשק Streamlit בעברית ובכיוון RTL
- טיפול מפורש בשגיאות ולוגים
- חבילת בדיקות רחבה עם סף Coverage מינימלי של 90%
- GitHub Actions לבדיקות אוטומטיות בכל Push ובכל Pull Request

## Presets מובנים

הפרויקט כולל 12 סגנונות מוכנים:

- מותאם אישית
- Cyber Pulse
- Dream Portal
- Broken Reality
- Liquid Signal
- Mirror Gloss
- Dramatic Black & White
- Cinema Noir
- Chrome Tunnel
- Neon Fracture
- Electric Wave
- Infinite Reflection

הסגנונות Dramatic Black & White ו-Cinema Noir משתמשים באפקט
`GrayscaleEffect` עצמאי, הרשום ב-Registry כמו שאר האפקטים.

## דרישות מוקדמות

- Git
- UV
- Python 3.12, או אפשרות ל-UV להתקין אותו אוטומטית

בדיקת ההתקנה:

```bash
uv --version
```

## התקנה והרצה

שכפול הפרויקט:

```bash
git clone git@github.com:hagayo/reality-glitch-studio.git
cd reality-glitch-studio
```

התקנת סביבת העבודה והתלויות:

```bash
uv sync
```

הפקודה יוצרת את `.venv` ואת `uv.lock`. יש לצרף את `uv.lock` ל-Git כדי
שההתקנות המקומיות וההרצות ב-CI ישתמשו באותן גרסאות מדויקות.

הרצת האפליקציה:

```bash
uv run streamlit run app.py
```

האפליקציה תיפתח בדרך כלל בכתובת:

```text
http://localhost:8501
```

## שימוש באפליקציה

1. מעלים תמונת JPG, PNG או WEBP.
2. בוחרים Preset מוכן או מרכיבים Pipeline אישי.
3. משנים את הגדרות האפקטים והגימור.
4. בוחנים את תוצאת הביניים של כל שלב.
5. מורידים PNG או יוצרים GIF מונפש.

התמונה מוגבלת לגודל מרבי כדי לשמור על זמן עיבוד וצריכת זיכרון סבירים.

## ארכיטקטורה

```text
app.py
src/reality_glitch/
├── domain/
│   ├── models.py          מודלים בלתי תלויים בממשק
│   ├── ports.py           חוזים ו-Protocols
│   └── exceptions.py      חריגות ייעודיות
├── effects/
│   ├── wave.py
│   ├── glitch.py
│   ├── rgb_split.py
│   ├── mirror.py
│   ├── portal.py
│   └── grayscale.py
├── services/
│   ├── image_service.py
│   ├── pipeline_service.py
│   ├── animation_service.py
│   └── export_service.py
├── infrastructure/
│   ├── registry.py
│   └── presets.py
├── ui/
│   ├── controls.py
│   ├── state.py
│   └── styles.py
└── container.py           Composition Root ו-Dependency Injection
```

### זרימת התלויות

```text
Streamlit UI
    ↓
Application services
    ↓
Domain contracts
    ↑
Effects and infrastructure implementations
```

שכבת הדומיין אינה תלויה ב-Streamlit. שירות ה-Pipeline אינו מכיר אפקטים
קונקרטיים, אלא עובד דרך `EffectRegistry`. שירות האנימציה תלוי בחוזים של
ה-Pipeline וה-Registry ולא במחלקות המימוש עצמן.

## עקרונות SOLID

- **SRP** - לכל אפקט ולכל שירות אחריות אחת מוגדרת.
- **OCP** - ניתן להוסיף אפקט חדש ללא שינוי במנוע ה-Pipeline.
- **LSP** - כל אפקט ניתן להחלפה דרך החוזה `ImageEffect`.
- **ISP** - קיימים חוזים קטנים ונפרדים ל-Registry, Pipeline, Presets, Export ו-Animation.
- **DIP** - השירותים תלויים ב-Protocols ולא במחלקות קונקרטיות.

## הוספת אפקט חדש

1. מוסיפים מזהה חדש ל-`EffectId`.
2. יוצרים מחלקה חדשה בתיקיית `effects`.
3. מממשים את החוזה `ImageEffect` או יורשים מ-`BaseEffect`.
4. מוסיפים את האפקט ל-Registry בתוך `container.py`.
5. מוסיפים בקרות מתאימות ב-`ui/controls.py`.
6. מוסיפים בדיקות יחידה, בדיקות מקרי קצה ובדיקת Pipeline.

אין צורך להוסיף תנאים חדשים ל-`ImagePipelineService` או ל-`GifAnimationService`.

## הוספת Preset

Preset מוגדר ב-`infrastructure/presets.py` ומכיל:

- שם
- רשימת `EffectStep` לפי סדר ההפעלה
- הגדרות לכל אפקט
- הגדרות גימור

יש להוסיף בדיקה שמוודאת שכל אפקט ב-Preset רשום ב-Registry ושכל הערכים חוקיים.

## בדיקות

הרצת כל הטסטים:

```bash
uv run pytest
```

הרצה עם Coverage:

```bash
uv run pytest \
  --cov=reality_glitch \
  --cov-report=term-missing \
  --cov-report=html
```

פתיחת דוח ה-HTML:

```text
htmlcov/index.html
```

הגדרת הפרויקט מכשילה את הבדיקות כאשר ה-Coverage יורד מתחת ל-90%.
חבילת הטסטים מכסה בין היתר:

- שמירת ממדי התמונה ואי-שינוי הקלט
- תמונות קטנות, RGBA וגווני אפור
- ערכים ניטרליים וערכים לא חוקיים
- דטרמיניזם של Glitch לפי Seed
- סדר שלבי Pipeline ותוצאות ביניים
- אפקט חסר, אפקט כפול ופלט אפקט לא תקין
- תקינות Presets מול ה-Registry
- פתיחה מחדש של PNG ו-GIF באמצעות Pillow
- מספר הפריימים בפועל ו-Ping-Pong
- בניית Dependency Container

שכבת התצוגה של Streamlit אינה חלק מסף ה-Coverage. ניתן להוסיף לה בהמשך
בדיקות `streamlit.testing.v1.AppTest` או בדיקות דפדפן כאשר התנהגות UI תהפוך
לחלק קריטי במוצר.

## בדיקות איכות

```bash
uv run ruff check .
uv run ruff format --check .
uv run python -m compileall -q app.py src tests
```

תיקון פורמט אוטומטי:

```bash
uv run ruff format .
```

## GitHub Actions

הקובץ `.github/workflows/ci.yml` מופעל אוטומטית על:

- Push לענף `main`
- Pull Request אל `main`
- הפעלה ידנית מתוך GitHub

ה-Workflow מבצע:

1. Checkout של הקוד.
2. התקנת UV ו-Python 3.12.
3. התקנת כל התלויות, כולל קבוצת הפיתוח.
4. בדיקת פורמט עם Ruff.
5. Lint עם Ruff.
6. קומפילציה של כל קובצי Python.
7. הרצת Pytest עם Coverage ו-Branch Coverage.
8. העלאת דוח Coverage כ-Artifact למשך 14 יום.

כאשר `uv.lock` קיים, ה-Workflow משתמש ב-`uv sync --locked`. כאשר הוא חסר,
ה-Workflow ממשיך לעבוד אך מציג אזהרה. בפרויקט משותף מומלץ תמיד לצרף אותו.

## פריסה ל-Streamlit Community Cloud

1. מעלים את הפרויקט ל-GitHub.
2. יוצרים אפליקציה חדשה ב-Streamlit Community Cloud.
3. בוחרים את ה-Repository ואת הענף `main`.
4. מגדירים את קובץ הכניסה כ-`app.py`.
5. בוחרים Python 3.12.
6. מבצעים Deploy.

אין צורך ב-`requirements.txt` כאשר `pyproject.toml` ו-`uv.lock` קיימים.

## פרטיות ומגבלות

- עיבוד התמונות מתבצע בזיכרון של תהליך Streamlit.
- הפרויקט אינו שומר תמונות במסד נתונים או באחסון קבוע.
- תמונות ו-GIF גדולים צורכים יותר זיכרון וזמן CPU.
- האפקטים מבוססים על עיבוד תמונה מתמטי ואינם משתמשים במודל AI.
- הפרויקט מיועד ללימוד ולהדגמה, ולא עבר בדיקות עומס של שירות Production רב-משתמשים.

## פתרון תקלות

### `uv` אינו מזוהה

```bash
uv --version
```

אם הפקודה נכשלת, יש להתקין UV ולפתוח מחדש את ה-Terminal.

### Import שגוי

הריצו פקודות דרך UV מתוך תיקיית השורש:

```bash
uv run pytest
uv run streamlit run app.py
```

### האפליקציה עובדת מקומית אך לא בענן

בדקו ש-`app.py`, `pyproject.toml`, `uv.lock`, תיקיית `src` וכל קובצי האפקטים
נמצאים ב-GitHub. Linux רגיש להבדלים בין אותיות גדולות וקטנות בשמות קבצים.

### ה-GIF איטי

הקטינו את מספר הפריימים, את גודל התמונה או את מספר האפקטים ב-Pipeline.

## רישיון

הפרויקט מופץ תחת רישיון MIT. ראו את הקובץ [LICENSE](LICENSE).

Copyright © 2026 Hagay Onn.
