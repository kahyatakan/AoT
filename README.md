# === Anvil of Taylor ===

**Herhangi bir matematiksel fonksiyonun Taylor serisi açılımını otomatik hesaplayan, görselleştiren ve sayısal değerlendirme yapan Python aracı. LaTeX ile fonksiyon yazın, sonucu anında görün — tarayıcıda veya Jupyter'da.**

---

## Bu Araç Ne İşe Yarıyor?

Diyelim ki elinizde karmaşık bir matematiksel fonksiyon var — örneğin `f(x) = sin(x)` ya da `f(x₁, x₂) = e^(x₁² + x₂²)`. Bu fonksiyonlar güzel ama hesaplaması zor. Taylor serisi, bu karmaşık fonksiyonları **belirli bir noktanın etrafında basit bir polinomla yaklaşık olarak ifade etmenizi** sağlar.

### Günlük hayattan bir benzetme

Bir tepenin üzerinde durduğunuzu düşünün. Ayaklarınızın altındaki küçük bölgeyi düz bir zemin gibi düşünebilirsiniz — bu **1. derece** yaklaşımdır. Biraz daha geniş bakarsanız, yüzeyin hafifçe kavisli olduğunu fark edersiniz ve onu bir kase (paraboloid) gibi modellersiniz — bu **2. derece** yaklaşımdır. İşte Taylor serisi tam olarak bunu yapar: karmaşık bir yüzeyi, bir noktanın komşuluğunda basit bir polinomla taklit eder.

### AOT ne yapıyor?

1. **Siz bir fonksiyon ve bir açılım noktası veriyorsunuz** — LaTeX ile veya Python kodu ile.
2. **AOT, o noktadaki Taylor açılımını sembolik olarak hesaplıyor** — yani sonuç sayı değil, matematiksel bir formül.
3. **İsterseniz sayısal değer alıyorsunuz** — formülü herhangi bir noktada hesaplatabilirsiniz.
4. **İsterseniz grafik çizdiriyorsunuz** — orijinal fonksiyon ile Taylor yaklaşımını üst üste görerek ne kadar iyi çalıştığını gözlemliyorsunuz.

Tüm bunları **1 değişkenli**, **2 değişkenli** ve **3 değişkenli** fonksiyonlar için yapabilirsiniz.

### İki kullanım yolu

```
┌──────────────────────────────────────────────────┐
│  Yol 1: Web Arayüzü (Python bilmeden)            │
│  Tarayıcıda LaTeX yazın → sonuç anında gelir     │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  Yol 2: Python / Jupyter (tam kontrol)           │
│  import aot → sembolik, sayısal, grafik          │
└──────────────────────────────────────────────────┘
```

---

## Kurulum

### Gereksinimler

- **Python 3.10 veya üstü** — hem Python yolu hem web arayüzünün backend'i için.
- **Node.js 18 veya üstü** — yalnızca web arayüzünü çalıştırmak istiyorsanız. [nodejs.org](https://nodejs.org) adresinden indirin.
- pip (Python paket yöneticisi — Python ile birlikte gelir)

### 1. Repoyu bilgisayarınıza indirin

```bash
git clone https://github.com/kahyatakan/AoT.git
cd AoT
```

### 2. (Tavsiye edilir) Sanal ortam oluşturun

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

### 3. Python paketini kurun

```bash
# Temel kurulum (sembolik hesap + matplotlib grafikleri):
pip install -e .

# Ekstra: interaktif 3D grafikler (plotly) dahil — tavsiye edilir:
pip install -e ".[viz]"

# Ekstra: Jupyter notebook desteği dahil:
pip install -e ".[notebook]"

# Ekstra: gelişmiş LaTeX parse desteği (latex2sympy2):
pip install -e ".[latex]"

# Hepsini birden:
pip install -e ".[viz,notebook,latex]"
```

> **`-e .` ne demek?** "Editable install" — paketi kurar ama dosyaları yerinde bırakır. Kodda değişiklik yaparsanız tekrar kurmanız gerekmez, değişiklikler anında yansır.

### 4. Kurulumun çalıştığını test edin

```bash
python -c "from aot import TaylorExpansion; print('AOT hazır!')"
```

`AOT hazır!` yazısını gördüyseniz her şey yolunda.

---

## Web Arayüzü (Python bilmeden kullanım)

Python bilmeden AOT'u kullanmak istiyorsanız web arayüzü tam size göre. Tarayıcıda LaTeX ile fonksiyon yazıyorsunuz, Taylor açılımı ve grafiği anında karşınıza geliyor.

### Web arayüzünü başlatmak

İki terminal penceresi açın:

**Terminal 1 — Arka uç (backend):**

```bash
# AoT klasöründe olduğunuzdan emin olun
pip install fastapi uvicorn
python -m uvicorn server.main:app --reload --port 8000
```

Başarılıysa şunu görürsünüz:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 — Ön yüz (frontend):**

```bash
cd web
npm install   # ilk seferinde gerekli (bağımlılıkları indirir)
npm run dev
```

Başarılıysa şunu görürsünüz:
```
VITE ready in 200ms
➜  Local: http://localhost:5173/
```

Tarayıcınızda `http://localhost:5173` adresini açın. Hazır!

### Web arayüzünde ne var?

```
┌─────────────────────────────────────────────────────┐
│  Fonksiyon girişi                                   │
│  ┌─────────────────────────────────────────────┐    │
│  │  sin(x)  ← LaTeX editörde WYSIWYG yazın    │    │
│  └─────────────────────────────────────────────┘    │
│  [sin(x)]  [e^x²]  [2D karmaşık]  [3D örnek]       │
│                                                     │
│  Açılım noktası     Mertebe                         │
│  x = [  0  ]        [──●────] 5                    │
│                                                     │
│  [      Hesapla      ]                              │
├─────────────────────────────────────────────────────┤
│  Taylor açılımı:                                    │
│  x - x³/6 + x⁵/120                                 │
│                                                     │
│  [  İnteraktif Plotly grafiği  ]                    │
└─────────────────────────────────────────────────────┘
```

- **LaTeX editör (MathLive):** Formülleri görsel olarak yazın. `\sin`, `\frac`, `^`, `_` gibi LaTeX komutları otomatik render edilir.
- **Örnek butonlar:** Hazır fonksiyonları tek tıkla editöre yükleyin.
- **Açılım noktası:** 1D, 2D veya 3D seçin; koordinatları girin.
- **Mertebe seçici:** 1D için 1–100 arası kaydırıcı; 2D/3D için sabit 2.
- **Sonuç:** KaTeX ile render edilmiş formül + gradient + Hessian.
- **Grafik:** Plotly ile interaktif — döndürme, yakınlaştırma, veri üzerinde hover.
- **Hata mesajları:** LaTeX sözdizimi hatası, tanımsız nokta gibi durumlarda açıklayıcı Türkçe mesaj.

### REST API olarak kullanım

Backend'i başlattıktan sonra doğrudan HTTP isteği de atabilirsiniz:

```bash
curl -X POST http://localhost:8000/api/expand \
  -H "Content-Type: application/json" \
  -d '{"latex": "\\sin(x)", "point": [0.0], "order": 5}'
```

Yanıt:
```json
{
  "status": "ok",
  "symbolic_latex": "x - \\frac{x^3}{6} + \\frac{x^5}{120}",
  "variables": ["x"],
  "dimension": 1,
  "gradient_latex": null,
  "hessian_latex": null,
  "plot_json": { "data": [...], "layout": {...} }
}
```

---

## Python ile Kullanım

### LaTeX string ile (en kolay yol)

v2'de eklenen `from_latex` class methodu ile doğrudan LaTeX string'i kullanabilirsiniz. Değişkenleri bile otomatik tespit eder:

```python
from aot import TaylorExpansion

# sin(x) — değişkeni (x) otomatik bulur
T = TaylorExpansion.from_latex(r"\sin(x)", point=[0], order=5)
print(T.symbolic)
# x - x**3/6 + x**5/120

# Kesirli 2D fonksiyon — x1 ve x2'yi otomatik bulur
T2 = TaylorExpansion.from_latex(
    r"\frac{e^{x_1^2 + x_2^2}}{\sin(x_1) \cdot \cos(x_2)}",
    point=[1, 0.5],
    order=2
)
print(T2.gradient)
```

> **`r"..."` ne demek?** Python'da raw string. Ters eğik çizgileri (`\`) LaTeX komutu olarak yorumlamasını sağlar. LaTeX yazarken her zaman `r"..."` kullanın.

### Sympy ifadesi ile (tam kontrol)

```python
import sympy as sp
from aot import TaylorExpansion

x = sp.Symbol('x')

T = TaylorExpansion(
    f=sp.sin(x),       # sympy ifadesi
    variables=[x],      # değişken listesi
    point=[0],          # açılım noktası
    order=5             # mertebe
)
```

---

## Örnekler

### Örnek 1 — 1D: sin(x) açılımı

```python
from aot import TaylorExpansion

T = TaylorExpansion.from_latex(r"\sin(x)", point=[0], order=5)

print(T.symbolic)
# x - x**3/6 + x**5/120

print(T.latex())
# \frac{x^{5}}{120} - \frac{x^{3}}{6} + x

# Grafik: orijinal sin(x) vs Taylor yaklaşımı üst üste
fig = T.plot()
```

Grafik size şunu gösterir:
- **Mavi çizgi:** Gerçek `sin(x)` fonksiyonu
- **Kırmızı kesikli çizgi:** 5. derece Taylor yaklaşımı
- **Kırmızı nokta:** Açılım noktası (x = 0)

Açılım noktasının yakınında iki çizgi neredeyse üst üste gelir; uzaklaştıkça ayrılır. Bu, Taylor serisinin doğasıdır: **yakında çok iyi, uzakta kötü**.

---

### Örnek 2 — 1D: eˣ açılımı, yüksek mertebe

```python
T = TaylorExpansion.from_latex(r"e^{x}", point=[0], order=20)

# 20 terim çok uzun — varsayılan olarak ilk 10 gösterilir
print(T.latex())             # ilk 10 terim + \cdots

# Kaç terim gösterileceğini kendiniz seçin
print(T.latex(max_terms=4))  # 1 + x + x²/2 + x³/6 + \cdots
print(T.latex(max_terms=None))  # tüm 21 terim (uzun!)

# Belirli bir noktada değer hesapla
import sympy as sp
x = sp.Symbol('x')
print(T.evaluate({x: 1}))   # → 1 + 1 + 1/2 + 1/6 + ... ≈ e
```

> **1D'de mertebe sınırı nedir?** 1 ile 1000 arasında herhangi bir değer girebilirsiniz. 100'ün üzerinde bir uyarı çıkar ama hesaplama devam eder.

---

### Örnek 3 — 2D: iki değişkenli fonksiyon

`f(x₁, x₂) = e^(x₁² + x₂²)` fonksiyonunu `(1, 0)` noktasında açalım:

```python
from aot import TaylorExpansion

T = TaylorExpansion.from_latex(
    r"e^{x_1^2 + x_2^2}",
    point=[1, 0],
    order=2
)

# Sembolik Taylor açılımı (2. derece polinom)
print(T.symbolic)

# Gradient — fonksiyonun o noktadaki "en dik artış yönü"
print(T.gradient)

# Hessian — fonksiyonun o noktadaki eğrilik matrisi
print(T.hessian)

# Sayısal değerlendirme
import sympy as sp
x1, x2 = sp.symbols('x1 x2')
print(T.evaluate({x1: 1.1, x2: 0.2}))

# 3D interaktif grafik (plotly gerekir)
fig = T.plot()
```

Grafik **3 boyutlu** olur:
- **Yarı-saydam mavi yüzey:** Gerçek fonksiyon
- **Yarı-saydam kırmızı yüzey:** Taylor yaklaşımı (paraboloid)
- **Kırmızı nokta:** Açılım noktası (1, 0)

İki yüzeyin açılım noktasının yakınında nasıl örtüştüğünü, uzaklaştıkça nasıl ayrıldığını görebilirsiniz.

> **2D'de mertebe sınırı nedir?** Şimdilik yalnızca `order=2` desteklenmektedir. `order=3` verirseniz hata alırsınız. Yüksek dereceli çok değişkenli açılım gelecek sürümlerde eklenecektir.

---

### Örnek 4 — 2D: karmaşık fonksiyon

```python
T = TaylorExpansion.from_latex(
    r"\frac{e^{x_1^2 + x_2^2}}{\sin(x_1) \cdot \cos(x_2)}",
    point=[1, 0.5],
    order=2
)

print(T.symbolic)
print(T.gradient)
print(T.hessian)
fig = T.plot()
```

---

### Örnek 5 — 3D: üç değişkenli fonksiyon

```python
from aot import TaylorExpansion

T = TaylorExpansion.from_latex(
    r"x_1 \cdot x_2 \cdot x_3",
    point=[1, 1, 1],
    order=2
)

print(T.symbolic)

import sympy as sp
x1, x2, x3 = sp.symbols('x1 x2 x3')
print(T.evaluate({x1: 1.1, x2: 0.9, x3: 1.2}))
```

> **Not:** 3 değişkenli fonksiyonlar için grafik çizilemez (4 boyutlu bir uzay gerekir). `T.plot()` çağırırsanız açıklayıcı bir hata mesajı alırsınız.

---

### Örnek 6 — Sembolik açılım noktası

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
# exp(a) + (x - a)*exp(a) + (x - a)**2*exp(a)/2
# Bu, eˣ'in genel Taylor formülüdür!
```

---

### Örnek 7 — Sayısal değerlendirme ve hızlı hesap

```python
import numpy as np
from aot import TaylorExpansion

T = TaylorExpansion.from_latex(r"e^{x}", point=[0], order=5)

# Tek bir noktada
import sympy as sp
x = sp.Symbol('x')
print(T.evaluate({x: 0.5}))   # → sembolik hesap

# Hızlı numpy uyumlu fonksiyon (büyük veri için ideal)
f_num = T.to_numeric()           # orijinal fonksiyon
taylor_num = T.taylor_to_numeric()  # Taylor yaklaşımı

xs = np.linspace(-2, 2, 1000)
print(f_num(xs))         # orijinal eˣ değerleri
print(taylor_num(xs))    # Taylor yaklaşımı değerleri
```

---

## Jupyter Notebook'ta Kullanım

AOT, Jupyter notebook ile en iyi şekilde çalışır. Özel bir şey yapmanıza gerek yok — sonuçlar otomatik olarak güzel görünür:

```python
# Bir Jupyter hücresinde sadece T yazın:
T
```

Bu, LaTeX ile derlenmiş matematiksel formülü doğrudan notebook'ta render eder.

### Hazır Notebook Örnekleri

`notebooks/` klasöründe adım adım örnekler bulunur:

| Notebook | Açıklama |
|---|---|
| `01_1d_example.ipynb` | Tek değişkenli fonksiyonlarla başlangıç, yüksek mertebe, grafik |
| `02_2d_example.ipynb` | İki değişkenli fonksiyonlar, gradient, Hessian, 3D görselleştirme |
| `03_3d_example.ipynb` | Üç değişkenli fonksiyonlar (sembolik + sayısal) |

Notebook'ları açmak için:

```bash
pip install -e ".[notebook]"
jupyter notebook notebooks/
```

---

## LaTeX Parser

v2'de eklenen bu özellik sayesinde LaTeX string'ini doğrudan `from_latex()` ile kullanabilirsiniz. Parser aşağıdaki tüm kalıpları destekler:

| LaTeX girdi | Sympy karşılığı |
|---|---|
| `\sin(x)` | `sp.sin(x)` |
| `\cos(x_1)` | `sp.cos(x1)` |
| `\tan(x)` | `sp.tan(x)` |
| `\arctan(x)` | `sp.atan(x)` |
| `\ln(x)` | `sp.log(x)` |
| `e^{x}` | `sp.exp(x)` |
| `e^{x^2 + y^2}` | `sp.exp(x**2 + y**2)` |
| `\frac{a}{b}` | `a / b` |
| `\sqrt{x}` | `sp.sqrt(x)` |
| `x^2` | `x**2` |
| `x_1^2` | `x1**2` |
| `x_1 \cdot x_2` | `x1 * x2` |
| `\pi` | `sp.pi` |

**Değişkenler otomatik tespit edilir:** Parser, ifadedeki serbest sembolleri bulur ve alfabetik sıraya göre döndürür (`x < x1 < x2 < y < z`).

---

## API Referansı

### `TaylorExpansion` Sınıfı

#### Oluşturma — iki yol

```python
# Yol 1: LaTeX string ile (önerilen)
T = TaylorExpansion.from_latex(latex, point, order=2)

# Yol 2: Sympy ifadesi ile
T = TaylorExpansion(f, variables, point, order=2)
```

#### Parametreler

| Parametre | Tip | Açıklama |
|---|---|---|
| `latex` | `str` | LaTeX string (raw string kullanın: `r"\sin(x)"`) |
| `f` | `sympy.Expr` | Sympy ifadesi |
| `variables` | `list[sympy.Symbol]` | Değişken listesi (1–3 eleman) |
| `point` | `list` | Açılım noktası — **zorunlu, varsayılan yok**. Sayısal (`[1, 0]`) veya sembolik (`[a1, a2]`). |
| `order` | `int` | Mertebe. 1D'de 1–1000 serbest; 2D/3D'de yalnızca `2`. |

#### Özellikler

| Özellik | Açıklama |
|---|---|
| `.symbolic` | Sadeleştirilmiş Taylor açılım ifadesi (sympy.Expr) |
| `.gradient` | Gradient vektörü — yalnızca 2D/3D; 1D'de `None` |
| `.hessian` | Hessian matrisi — yalnızca 2D/3D; 1D'de `None` |

#### Metodlar

| Metod | Açıklama |
|---|---|
| `.latex(max_terms=10)` | Taylor ifadesinin LaTeX string'i. `max_terms=None` ile tüm terimler. |
| `.evaluate(values)` | Verilen noktada sayısal değer. `values = {x1: 1.5, x2: 0.3}` |
| `.to_numeric()` | Orijinal fonksiyonun numpy uyumlu versiyonu |
| `.taylor_to_numeric()` | Taylor yaklaşımının numpy uyumlu versiyonu |
| `.plot(**kwargs)` | Grafik döndürür. `output="json"` ile Plotly JSON dict. |

#### `plot()` parametreleri

| Parametre | Varsayılan | Açıklama |
|---|---|---|
| `output` | `"figure"` | `"figure"` → figure nesnesi; `"json"` → Plotly JSON dict |
| `xlim` | nokta ± 3 | 1D için x eksen sınırları, ör. `(-5, 5)` |
| `resolution` | `200` | Grafikteki nokta sayısı |

---

## Sıkça Sorulan Sorular

### "Taylor serisi" ne demek?

Karmaşık bir fonksiyonu, belirli bir noktanın etrafında **basit bir polinomla** yaklaşık olarak ifade etme yöntemidir. Polinom derecesi arttıkça yaklaşım iyileşir. Tek değişkenli fonksiyonlarda AOT 1000. dereceye kadar çıkabilir; çok değişkenli fonksiyonlarda şimdilik 2. derece desteklenir.

### "Açılım noktası" ne demek ve neden zorunlu?

Taylor serisi her zaman **belirli bir noktanın komşuluğunda** geçerlidir. O nokta açılım noktasıdır. Orijin (sıfır noktası) için `point=[0]` yazın — bu özel bir durum değil, sadece sıfırda açılım yapmaktır.

### "Sembolik" ve "sayısal" ne demek?

- **Sembolik**: Sonuç bir formüldür, sayı değil. Örneğin `x - x³/6 + x⁵/120`. Bunu kağıda yazabilirsiniz.
- **Sayısal**: Formüle belirli bir sayı koyup hesap yaparsınız. Örneğin `x = 0.5` koyunca sayısal bir değer çıkar.

AOT ikisini de yapar. Sembolik hesap `sympy`, sayısal hesap `numpy` ile yapılır.

### "Gradient" ve "Hessian" ne demek?

- **Gradient**: Fonksiyonun bir noktadaki **en dik artış yönünü** gösteren vektör. Bir tepede duruyorsanız gradient "zirveye giden yön"dür.
- **Hessian**: Fonksiyonun bir noktadaki **eğrilik bilgisini** tutan matris. Yüzeyin o noktada ne kadar ve hangi yönlerde kavisli olduğunu söyler. Taylor açılımının 2. derece terimini oluşturur.

Gradient ve Hessian yalnızca 2D ve 3D fonksiyonlarda hesaplanır; 1D'de `None` döner.

### Neden 2D/3D'de sadece 2. derece?

2. derece (kuadratik) yaklaşım, çok değişkenli fonksiyonlarda en yaygın kullanılandır — optimizasyon algoritmalarının çoğu (Newton metodu gibi) bu seviyede çalışır. Tek değişkenli fonksiyonlarda ise istediğiniz dereceye (1000'e kadar) çıkabilirsiniz. Çok değişkenli yüksek dereceler gelecek sürümlerde eklenecektir.

### Plotly kurmam şart mı?

Hayır. Plotly kurulu değilse AOT otomatik olarak matplotlib'e döner. Ama 2D fonksiyonların 3D grafiklerinde plotly çok daha iyi bir deneyim sunar (döndürme, yakınlaştırma, hover), bu yüzden `pip install -e ".[viz]"` ile kurmanızı öneririz.

### LaTeX'te `x_1` mi yazmalıyım, `x1` mi?

İkisi de çalışır. Parser hem `x_1` hem `x1` notasyonunu tanır ve her ikisini de `x1` sembolüne dönüştürür. Web arayüzünde MathLive editör otomatik olarak güzel format uygular.

### `from_latex` ile `TaylorExpansion(f=...)` arasındaki fark ne?

Sadece giriş formatı farklıdır. İkisi de aynı sınıfı oluşturur, aynı özelliklere ve metodlara sahiptir. LaTeX yazıyorsanız `from_latex` daha kısa ve kolaydır. Sympy ifadesi ile çalışıyorsanız (programatik kullanım) doğrudan constructor uygundur.

---

## Proje Yapısı

```
AoT/
├── aot/                    ← Python paketi (çekirdek motor)
│   ├── __init__.py         ← Dışarıya açılan public API
│   ├── core.py             ← TaylorExpansion sınıfı (sembolik motor)
│   ├── parser.py           ← LaTeX → sympy dönüştürücü (v2)
│   ├── numerical.py        ← lambdify sarmalayıcı, sayısal değerlendirme
│   ├── visualization.py    ← matplotlib/plotly ile görselleştirme
│   └── utils.py            ← Girdi doğrulama, yardımcı fonksiyonlar
│
├── server/                 ← FastAPI backend (v2)
│   ├── main.py             ← /api/expand endpoint, CORS, timeout
│   ├── schemas.py          ← Pydantic request/response modelleri
│   └── requirements.txt    ← fastapi, uvicorn, pydantic
│
├── web/                    ← React frontend (v2)
│   ├── src/
│   │   ├── App.jsx                    ← Ana uygulama
│   │   ├── api/client.js              ← Backend ile HTTP iletişimi
│   │   ├── components/
│   │   │   ├── FunctionInput.jsx      ← MathLive LaTeX editör
│   │   │   ├── PointInput.jsx         ← Boyut + koordinat girişi
│   │   │   ├── OrderInput.jsx         ← Mertebe seçici
│   │   │   ├── ResultDisplay.jsx      ← KaTeX ile formül render
│   │   │   ├── PlotDisplay.jsx        ← Plotly.js ile grafik
│   │   │   └── ErrorDisplay.jsx       ← Hata mesajları
│   │   └── styles/main.css
│   ├── package.json
│   └── vite.config.js
│
├── notebooks/              ← Jupyter örnekleri
│   ├── 01_1d_example.ipynb
│   ├── 02_2d_example.ipynb
│   └── 03_3d_example.ipynb
│
├── tests/                  ← Otomatik testler (88 test)
│   ├── test_core.py
│   ├── test_parser.py
│   ├── test_numerical.py
│   ├── test_visualization.py
│   └── test_api.py
│
├── pyproject.toml          ← Paket ayarları ve bağımlılıklar
├── README.md               ← Bu dosya
└── LICENSE                 ← MIT lisansı
```

---

## Geliştirme & Katkı

```bash
# Geliştirme modunda kur
pip install -e ".[dev,viz,latex,notebook]"

# Tüm testleri çalıştır (88 test)
pytest tests/ -v

# Belirli bir test dosyasını çalıştır
pytest tests/test_parser.py -v

# Backend'i başlat
python -m uvicorn server.main:app --reload --port 8000

# Frontend'i başlat
cd web && npm run dev
```

Katkıda bulunmak isterseniz: repoyu forklayın, değişikliklerinizi yapın, testleri çalıştırın (`pytest tests/ -v` → hepsi geçmeli), ardından PR açın.

---

## Lisans

MIT — dilediğiniz gibi kullanın, değiştirin, dağıtın.
