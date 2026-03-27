# === Anvil of Taylor ===

**Herhangi bir matematiksel fonksiyonun Taylor serisi açılımını otomatik hesaplayan, görselleştiren ve sayısal değerlendirme yapan Python aracı.**

---

## Bu Araç Ne İşe Yarıyor?

Diyelim ki elinizde karmaşık bir matematiksel fonksiyon var — örneğin `f(x) = eˣ` ya da `f(x₁, x₂) = e^(x₁² + x₂²)`. Bu fonksiyonlar güzel ama hesaplaması zor. Taylor serisi, bu karmaşık fonksiyonları **belirli bir noktanın etrafında basit bir polinomla yaklaşık olarak ifade etmenizi** sağlar.

### Günlük hayattan bir benzetme

Bir tepenin üzerinde durduğunuzu düşünün. Ayaklarınızın altındaki küçük bölgeyi düz bir zemin gibi düşünebilirsiniz — bu **1. derece** yaklaşımdır. Biraz daha geniş bakarsanız, yüzeyin hafifçe kavisli olduğunu fark edersiniz ve onu bir kase (paraboloid) gibi modellersiniz — bu **2. derece** yaklaşımdır. İşte Taylor serisi tam olarak bunu yapar: karmaşık bir yüzeyi, bir noktanın komşuluğunda basit bir polinomla taklit eder.

### AOT ne yapıyor?

1. **Siz bir fonksiyon ve bir nokta veriyorsunuz.**
2. **AOT, o noktadaki Taylor açılımını sembolik olarak hesaplıyor** — yani sonuç sayı değil, matematiksel bir formül.
3. **İsterseniz sayısal değer alıyorsunuz** — formülü herhangi bir noktada hesaplatabilirsiniz.
4. **İsterseniz grafik çizdiriyorsunuz** — orijinal fonksiyon ile Taylor yaklaşımını üst üste görerek ne kadar iyi çalıştığını gözlemliyorsunuz.

Tüm bunları **1 değişkenli**, **2 değişkenli** ve **3 değişkenli** fonksiyonlar için yapabilirsiniz.

---

## Kurulum

### Gereksinimler

- Python 3.10 veya üstü
- pip (Python paket yöneticisi — Python ile birlikte gelir)

### Adım adım kurulum

**1. Repoyu bilgisayarınıza indirin:**

```bash
git clone https://github.com/KULLANICI_ADINIZ/aot.git
cd aot
```

**2. (Tavsiye edilir) Sanal ortam oluşturun:**

Sanal ortam, bu projenin bağımlılıklarını diğer projelerinizden izole eder. Zorunlu değil ama tavsiye edilir.

```bash
python -m venv .venv
```

Sanal ortamı aktif edin:

```bash
# macOS / Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

Aktif olduğunu anlamak için terminalinizin başında `(.venv)` yazısını görmelisiniz.

**3. Paketi kurun:**

```bash
# Temel kurulum (sembolik hesap + matplotlib grafikleri):
pip install -e .

# Ekstra: interaktif 3D grafikler (plotly) dahil:
pip install -e ".[viz]"

# Ekstra: Jupyter notebook desteği dahil:
pip install -e ".[notebook]"

# Hepsini birden:
pip install -e ".[viz,notebook]"
```

> **`-e .` ne demek?** "Editable install" — paketi kurar ama dosyaları yerinde bırakır. Kodda değişiklik yaparsanız tekrar kurmanız gerekmez, değişiklikler anında yansır.

**4. Kurulumun çalıştığını test edin:**

```bash
python -c "from aot import TaylorExpansion; print('AOT hazır!')"
```

`AOT hazır!` yazısını gördüyseniz her şey yolunda.

---

## Hızlı Başlangıç

### Örnek 1 — Tek değişkenli fonksiyon (1D)

`sin(x)` fonksiyonunu `x = 0` noktasında Taylor serisine açalım:

```python
import sympy as sp
from aot import TaylorExpansion

# 1. Değişkeni tanımla
x = sp.Symbol('x')

# 2. Taylor açılımını hesapla
T = TaylorExpansion(
    f=sp.sin(x),           # açmak istediğiniz fonksiyon
    variables=[x],          # değişken listesi
    point=[0],              # açılım noktası (x = 0)
    order=5                 # 5. dereceye kadar aç (1D'de 1000'e kadar gidebilir!)
)

# 3. Sembolik sonucu görün
print(T.symbolic)
# Çıktı: x - x³/6 + x⁵/120

# 4. LaTeX formatında görün (Jupyter'da otomatik render edilir)
print(T.latex())

# 5. Grafik çizdirin
fig = T.plot()
```

Bu kod şöyle bir grafik üretir:

- **Mavi çizgi:** Gerçek `sin(x)` fonksiyonu
- **Kırmızı kesikli çizgi:** Taylor yaklaşımı
- **Kırmızı nokta:** Açılım noktası (x = 0)

Grafikte göreceksiniz ki açılım noktasının yakınında iki çizgi neredeyse birbiriyle örtüşür, uzaklaştıkça ayrılır. Bu Taylor serisinin doğası gereğidir: **yakınlarda çok iyi, uzaklarda kötü** çalışır.

---

### Örnek 2 — İki değişkenli fonksiyon (2D)

`f(x₁, x₂) = e^(x₁² + x₂²)` fonksiyonunu `(1, 0)` noktasında açalım:

```python
import sympy as sp
from aot import TaylorExpansion

x1, x2 = sp.symbols('x1 x2')

T = TaylorExpansion(
    f=sp.exp(x1**2 + x2**2),
    variables=[x1, x2],
    point=[1, 0],
    order=2
)

# Sembolik sonuç
print(T.symbolic)

# Gradient vektörü (fonksiyonun o noktadaki "eğim yönü")
print(T.gradient)

# Hessian matrisi (fonksiyonun o noktadaki "eğrilik bilgisi")
print(T.hessian)

# Sayısal değerlendirme: x₁=1.1, x₂=0.2 noktasında Taylor yaklaşımının değeri
print(T.evaluate({x1: 1.1, x2: 0.2}))

# 3D görselleştirme (interaktif — döndürebilirsiniz)
fig = T.plot()
```

Bu sefer grafik **3 boyutlu** olur:

- **Yarı-saydam mavi yüzey:** Gerçek fonksiyon
- **Yarı-saydam kırmızı yüzey:** Taylor yaklaşımı (paraboloid)
- **Kırmızı nokta:** Açılım noktası (1, 0)

İki yüzeyin açılım noktası civarında nasıl örtüştüğünü, uzaklaştıkça nasıl ayrıldığını görebilirsiniz.

---

### Örnek 3 — Üç değişkenli fonksiyon (3D)

```python
import sympy as sp
from aot import TaylorExpansion

x1, x2, x3 = sp.symbols('x1 x2 x3')

T = TaylorExpansion(
    f=x1 * x2 * x3 + sp.sin(x1),
    variables=[x1, x2, x3],
    point=[0, 0, 0],
    order=2
)

# Sembolik sonuç
print(T.symbolic)

# Sayısal değerlendirme
print(T.evaluate({x1: 0.1, x2: 0.2, x3: 0.3}))
```

> **Not:** 3 değişkenli fonksiyonlar için grafik çizilemez (4 boyutlu bir uzay gerekir, bu da görselleştirilemez). `T.plot()` çağırırsanız sizi bilgilendiren bir hata mesajı alırsınız.

---

### Örnek 4 — Tamamen sembolik açılım

Açılım noktasını sayı yerine **sembol** olarak da verebilirsiniz. Bu, genel formülü görmek istediğinizde işe yarar:

```python
import sympy as sp
from aot import TaylorExpansion

x = sp.Symbol('x')
a = sp.Symbol('a')

T = TaylorExpansion(
    f=sp.exp(x),
    variables=[x],
    point=[a],          # "a" sembolik — sayı değil
    order=2
)

print(T.symbolic)
# Çıktı: exp(a) + (x - a)*exp(a) + (x - a)²*exp(a)/2
# Bu, eˣ'in genel Taylor formülüdür!
```

---

### Örnek 5 — Yüksek mertebe açılım (1D'nin gücü)

Tek değişkenli fonksiyonlarda açılım derecesini çok yükseğe çıkarabilirsiniz:

```python
# 50. dereceye kadar aç — sin(x)'in 0 civarında ne kadar iyi yaklaştığını görün
T = TaylorExpansion(
    f=sp.sin(x),
    variables=[x],
    point=[0],          # açılım noktası her zaman belirtilmeli
    order=50
)

# Sembolik ifade çok uzun olabilir — varsayılan olarak ilk 10 terim gösterilir
print(T.latex())             # ilk 10 terim + "..."
print(T.latex(max_terms=5))  # ilk 5 terim + "..."
print(T.latex(max_terms=None))  # cesaretliyseniz: tüm 26 terim

# Sayısal olarak kullanmak çok kolay
print(T.evaluate({x: 3.14159}))  # → ≈ 0 (pi civarında sin ≈ 0)

# Grafikte 50. derece yaklaşımın orijinal fonksiyona ne kadar yapıştığını görün
fig = T.plot()
```

> **Not:** Orijinde (sıfır noktasında) Taylor açılımı yapmak istiyorsanız `point=[0]` yazmanız yeterli. Bu, matematikte "Maclaurin serisi" olarak da bilinir, ama özünde sadece `a = 0` noktasındaki Taylor serisidir — ayrı bir kavram değil.

---

## Jupyter Notebook'ta Kullanım

AOT, Jupyter notebook ile en iyi şekilde çalışır. Notebook'ta özel bir şey yapmanıza gerek yok — sonuçlar otomatik olarak güzel görünür:

```python
# Bir Jupyter hücresinde sadece T yazın:
T
```

Bu, LaTeX ile derlenmiş matematiksel formülü doğrudan notebook'ta render eder.

### Hazır Notebook Örnekleri

`notebooks/` klasöründe adım adım örnekler bulunur:

| Notebook | Açıklama |
|---|---|
| `01_1d_example.ipynb` | Tek değişkenli fonksiyonlarla başlangıç |
| `02_2d_example.ipynb` | İki değişkenli fonksiyonlar ve 3D görselleştirme |
| `03_3d_example.ipynb` | Üç değişkenli fonksiyonlar (yalnızca sembolik + sayısal) |

Notebook'ları açmak için:

```bash
jupyter notebook notebooks/
```

---

## API Referansı

### `TaylorExpansion` Sınıfı

#### Oluşturma

```python
TaylorExpansion(f, variables, point, order=2)
```

| Parametre | Tip | Açıklama |
|---|---|---|
| `f` | `sympy.Expr` | Açılmak istenen fonksiyon. Sympy ifadesi olmalı. Kesirli, iç içe, her türlü fonksiyon girilebilir (ör. `sp.exp(x1**2) / sp.sin(x2)`). |
| `variables` | `list[sympy.Symbol]` | Fonksiyonun değişkenleri. 1 ile 3 arasında eleman. |
| `point` | `list` | Açılım noktası (**zorunlu**). Sayısal (ör. `[1, 0]`) veya sembolik (ör. `[a1, a2]`) olabilir. Orijin için `[0]` veya `[0, 0]` yazın. |
| `order` | `int` | Taylor açılımının derecesi. 1D fonksiyonlarda 1–1000 arası serbest. 2D ve 3D fonksiyonlarda şimdilik yalnızca `2` desteklenir. |

#### Özellikler (Properties)

| Özellik | Dönen Tip | Açıklama |
|---|---|---|
| `.symbolic` | `sympy.Expr` | Sadeleştirilmiş Taylor açılım ifadesi |
| `.gradient` | `sympy.Matrix` | Fonksiyonun açılım noktasındaki gradient vektörü |
| `.hessian` | `sympy.Matrix` | Fonksiyonun açılım noktasındaki Hessian matrisi |

#### Metodlar

| Metod | Dönen Tip | Açıklama |
|---|---|---|
| `.latex(max_terms=10)` | `str` | Taylor ifadesinin LaTeX string'i. `max_terms` ile gösterilecek terim sayısı sınırlanır; `None` verilirse tümü gösterilir. |
| `.evaluate(values)` | `float` | Verilen noktada Taylor yaklaşımının sayısal değeri. `values` bir dict: `{x1: 1.5, x2: 0.3}` |
| `.to_numeric()` | `callable` | Orijinal fonksiyonun hızlı sayısal versiyonu (numpy uyumlu) |
| `.taylor_to_numeric()` | `callable` | Taylor yaklaşımının hızlı sayısal versiyonu (numpy uyumlu) |
| `.plot(**kwargs)` | `Figure` | Orijinal fonksiyon ile Taylor yaklaşımını üst üste çizen grafik. 1D için matplotlib, 2D için plotly (veya matplotlib) kullanır. |

#### `plot()` parametreleri

| Parametre | Varsayılan | Açıklama |
|---|---|---|
| `xlim` | Açılım noktası ± 2 | 1D için x ekseninin sınırları, ör. `(-3, 3)` |
| `resolution` | `200` | Grafikteki nokta sayısı (yüksek = daha pürüzsüz) |
| `backend` | `"plotly"` (2D), `"matplotlib"` (1D) | Grafik kütüphanesi seçimi |

---

## Sıkça Sorulan Sorular

### "Taylor serisi" ne demek?

Karmaşık bir fonksiyonu, belirli bir noktanın etrafında **basit bir polinomla** yaklaşık olarak ifade etme yöntemidir. Polinom derecesi arttıkça yaklaşım iyileşir. AOT şu an 2. dereceye kadar destek verir; yani fonksiyonu sabit + doğrusal + kuadratik terimlerle yaklaşır.

### "Sembolik" ve "sayısal" ne demek?

- **Sembolik**: Sonuç bir formüldür, sayı değil. Örneğin `1 + x + x²/2`. Bunu kağıda yazabilirsiniz.
- **Sayısal**: Formüle belirli bir sayı koyup hesap yaparsınız. Örneğin `x = 0.5` koyunca `1.625` çıkar.

AOT ikisini de yapar. Sembolik hesap `sympy`, sayısal hesap `numpy` ile yapılır.

### "Gradient" ve "Hessian" ne demek?

- **Gradient**: Fonksiyonun bir noktadaki **en dik artış yönünü** gösteren vektör. Bir tepede duruyorsanız, gradient "zirveye giden yön"dür.
- **Hessian**: Fonksiyonun bir noktadaki **eğrilik bilgisini** tutan matris. Yüzeyin o noktada ne kadar ve hangi yönlerde kavisli olduğunu söyler. Taylor açılımının 2. derece terimini oluşturur.

### Neden 2D/3D'de sadece 2. derece?

2. derece (kuadratik) yaklaşım, çok değişkenli fonksiyonlarda en yaygın kullanılandır — optimizasyon algoritmalarının çoğu (Newton metodu gibi) bu seviyede çalışır. Tek değişkenli fonksiyonlarda ise istediğiniz dereceye (1000'e kadar) çıkabilirsiniz. Çok değişkenli yüksek dereceler gelecek sürümlerde eklenecektir.

### Plotly kurmam şart mı?

Hayır. Plotly kurulu değilse AOT otomatik olarak matplotlib'e döner. Ama 2D fonksiyonların 3D grafiklerinde plotly çok daha iyi bir deneyim sunar (döndürme, yakınlaştırma, etkileşimli inceleme), bu yüzden tavsiye edilir.

---

## Web Arayüzü

Python bilmeden de AOT'u kullanabilirsiniz. Tarayıcı tabanlı web arayüzü LaTeX ile fonksiyon girişi yapar, sembolik sonuç ve grafiği anında gösterir.

### Gereksinimler

- Python (backend) + Node.js (frontend) kurulu olmalı.

### Başlatma

```bash
# Terminal 1 — FastAPI backend
pip install fastapi uvicorn
uvicorn server.main:app --reload --port 8000

# Terminal 2 — React frontend
cd web
npm install
npm run dev   # → http://localhost:5173
```

Tarayıcıda `http://localhost:5173` adresini açın.

### Özellikler

- **MathLive editör**: WYSIWYG LaTeX giriş alanı — formülleri görsel olarak yazın.
- **Anlık render**: KaTeX ile Taylor açılımı, gradient ve Hessian formülleri ekranda render edilir.
- **İnteraktif grafik**: Plotly ile 1D/2D grafikler — döndürme, yakınlaştırma desteklenir.
- **Hata mesajları**: Parse hatası, tanımsız nokta, timeout gibi durumlarda açıklayıcı Türkçe mesaj.

### API

Backend bağımsız olarak da kullanılabilir:

```bash
curl -X POST http://localhost:8000/api/expand \
  -H "Content-Type: application/json" \
  -d '{"latex": "\\sin(x)", "point": [0.0], "order": 5}'
```

---

## Proje Yapısı

```
aot/
├── aot/                   ← Ana Python paketi
│   ├── __init__.py        ← Dışarıya açılan API
│   ├── core.py            ← TaylorExpansion sınıfı (sembolik motor)
│   ├── numerical.py       ← lambdify ile sayısal değerlendirme
│   ├── visualization.py   ← Grafik çizim fonksiyonları
│   └── utils.py           ← Yardımcı fonksiyonlar
├── server/                ← FastAPI backend
│   ├── main.py            ← API endpoint'leri
│   └── schemas.py         ← Pydantic modelleri
├── web/                   ← React frontend (Vite)
│   └── src/               ← Bileşenler, API istemcisi
├── notebooks/             ← Jupyter örnekleri
├── tests/                 ← Otomatik testler
├── CLAUDE.md              ← Geliştirme kılavuzu (Claude Code için)
├── pyproject.toml         ← Paket ayarları
├── README.md              ← Bu dosya
└── LICENSE                ← MIT lisansı
```

---

## Geliştirme & Katkı

Katkıda bulunmak isterseniz:

```bash
# Repoyu forklayın, klonlayın, sonra:
pip install -e ".[dev,viz,notebook]"

# Testleri çalıştırın:
pytest tests/ -v

# Tüm testler geçtikten sonra PR açın.
```

---

## Lisans

MIT — dilediğiniz gibi kullanın, değiştirin, dağıtın.
