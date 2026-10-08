# 🤖 Unitree G1 Datasets Hub — Categorized by Hand Type

ఈ వెబ్ అప్లికేషన్‌లో Unitree Robotics కి సంబంధించిన **146 manipulation datasets** ని చేతి వేళ్ల సంఖ్య (Finger Count) ప్రకారం 3 వర్గాలుగా విభజించాము:

1. 🖐️ **5-Finger Datasets (62 Datasets)**: Brainco & Inspire Five-Fingered Hands
2. 🤟 **3-Finger Datasets (13 Datasets)**: Dex3 Three-Fingered Dexterous Hand
3. ✌️ **2-Finger Datasets (71 Datasets)**: Dex1 Two-Fingered Parallel Gripper

---

## ➕ కొత్త dataset ఎలా add చేయాలి (How to add a dataset)

Website లోని ప్రతి card, `datasets/` folder లోని ఒక చిన్న `.json` file నుండి వస్తుంది. కొత్త file add చేస్తే website దానంతట అదే update అవుతుంది.

1. GitHub లో `datasets/` folder open చేసి **Add file → Create new file** నొక్కండి.
2. File పేరు `<dataset పేరు>.json` అని పెట్టండి, ఉదా: `G1_Dex1_Open_Drawer.json`
3. ఇది paste చేసి, మీ పేరు మరియు link మార్చండి:
   ```json
   {
     "name": "G1_Dex1_Open_Drawer",
     "url": "https://huggingface.co/datasets/your-name/G1_Dex1_Open_Drawer"
   }
   ```
4. **Commit changes** నొక్కండి. కొన్ని నిమిషాల్లో website లో కనిపిస్తుంది.

గమనికలు:

- `name` మరియు `url` తప్పనిసరి. `url` అనేది dataset అసలు ఉన్న చోటు link (videos / parquet files ఈ repo లో పెట్టకండి, GitHub 100 MB పైన files తీసుకోదు).
- పేరులో `Dex1`, `Dex3`, `Brainco` లేదా `Inspire` ఉంటే category దానంతట అదే వస్తుంది. లేకపోతే `"finger_category": "2_fingers"` (లేదా `"3_fingers"`, `"5_fingers"`) add చేయండి.
- కావాలంటే ఇవి కూడా ఇవ్వొచ్చు: `task_name`, `hand_type`, `downloads`, `likes`, `tags`.
- File లో తప్పు ఉంటే repo లోని **Actions** tab లో ఎర్ర ❌ కనిపిస్తుంది; దాని మీద click చేస్తే ఏ file లో ఏ తప్పో చూపిస్తుంది. తప్పు సరిచేసే వరకు website పాత data తోనే ఉంటుంది.
- `data.js` మరియు `categorized_datasets.json` ని చేత్తో edit చేయకండి; అవి `datasets/` నుండి automatic గా తయారవుతాయి (`python3 scripts/build_data.py`).

---

## 📁 ఫోల్డర్ లొకేషన్లు (Folder Locations)

ఈ ప్రాజెక్ట్ మీకు సులభంగా యాక్సెస్ అయ్యేలా సేవ్ చేయబడింది:

- **ప్రధాన ఫోల్డర్**: `/home/eswar/unitree-g1-datasets-web`
- **డెస్క్‌టాప్ షార్ట్‌కట్**: `/home/eswar/Desktop/Unitree_G1_Datasets_Web`
- **IDE Scratch Directory**: `/home/eswar/.gemini/antigravity-ide/scratch/unitree-g1-dataset-hub`

---

## 🚀 వెబ్ సైట్ ఎలా ఓపెన్ చేయాలి (How to Open / Run)

### విధానం 1: డైరెక్ట్‌గా బ్రౌజర్‌లో ఓపెన్ చేయడం (Offline / No Server Needed)
- ఫోల్డర్‌లోని `index.html` ఫైల్‌పై డబుల్ క్లిక్ చేయండి లేదా గూగుల్ క్రోమ్‌లో డ్రాగ్ చేయండి.
- `data.js` ద్వారా మొత్తం 146 డేటాసెట్లు ఆఫ్‌లైన్‌లో కూడా వెంటనే లోడ్ అవుతాయి!

### విధానం 2: లోకల్ సర్వర్‌తో (Recommended)
టెర్మినల్‌లో:
```bash
cd /home/eswar/unitree-g1-datasets-web
./start_server.sh
```
లేదా:
```bash
cd /home/eswar/unitree-g1-datasets-web
python3 -m http.server 8085
```
ఆ తర్వాత బ్రౌజర్‌లో 👉 **[http://localhost:8085](http://localhost:8085)** ఓపెన్ చేయండి.

---

## 📂 ఫోల్డర్‌లోని ఫైల్స్ వివరాలు:

- **`index.html`**: ప్రధాన వెబ్‌పేజీ UI (3-category layout, search, filters)
- **`style.css`**: ప్రీమియం డార్క్ మోడ్ స్టైలింగ్ & అట్రాక్టివ్ యానిమేషన్స్
- **`app.js`**: సెర్చ్, ఫిల్టరింగ్, కాపీ క్లోన్ కమాండ్స్ లాజిక్
- **`datasets/`**: ప్రతి dataset కి ఒక `.json` file (అసలు source)
- **`scripts/build_data.py`**: `datasets/` నుండి `data.js` మరియు `categorized_datasets.json` తయారు చేస్తుంది
- **`.github/workflows/update-site.yml`**: push అయిన ప్రతిసారి website ని rebuild చేసి publish చేస్తుంది
- **`data.js`**: ఆఫ్‌లైన్ లోడింగ్ కోసం డేటాసెట్స్ డేటా
- **`categorized_datasets.json`**: 146 డేటాసెట్ల పూర్తి JSON సమాచారం
- **`start_server.sh`**: సింగిల్ క్లిక్ సర్వర్ స్టార్ట్ స్క్రిప్ట్
- **`download_dataset.py`**: డేటాసెట్‌లను వేగంగా డౌన్‌లోడ్ చేసే పైథాన్ స్క్రిప్ట్
