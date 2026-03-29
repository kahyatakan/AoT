# 🔨 AOT — Anvil of Taylor

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

### Ön Gereksinimler

Başlamadan önce şunların kurulu olduğundan emin olun:

- **Python 3.10+** → `python --version` ile kontrol edin
- **pip** → Python ile birlikte gelir, `pip --version` ile kontrol edin
- **Node.js 18+** ve **npm** (sadece web arayüzü için) → `node --version` ve `npm --version` ile kontrol edin

Node.js kurulu değilse işletim sisteminize göre:

| İşletim Sistemi | Kurulum komutu |
|---|---|
| **Fedora / RHEL** | `sudo dnf install nodejs npm` |
| **Ubuntu / Debian** | `sudo apt install nodejs npm` |
| **Arch Linux** | `sudo pacman -S nodejs npm` |
| **macOS** | `brew install node` |
| **Windows** | [nodejs.org](https://nodejs.org) adresinden LTS sürümünü indirip kurun |

> **Not:** Web arayüzünü kullanmayacaksanız Node.js gerekmez — sadece Python yeterlidir.

### Adım adım kurulum

**1. Repoyu bilgisayarınıza indirin:**

```bash
git clone https://github.com/kahyatakan/AoT
cd aot
```

**2. Sanal ortam oluşturun (ZORUNLU):**

AOT'un bağımlılıklarını sisteminizden izole etmek için sanal ortam şarttır. Özellikle **conda kullanıyorsanız**, conda ortamı ile sanal ortam karışabilir — aşağıdaki adımları mutlaka uygulayın.

```bash
python -m venv .venv
```

Sanal ortamı aktif edin:

```bash
# macOS / Linux:
source .venv/bin/activate

# Windows (CMD):
.venv\Scripts\activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

Aktif olduğunu anlamak için terminalinizin başında `(.venv)` yazısını görmelisiniz.

> **Conda kullanıcıları için önemli uyarı:** Eğer terminalinizde `(base)` yazıyorsa, conda'nın base ortamı aktiftir. `.venv`'i aktif ettiğinizde `(.venv) (base)` gibi bir şey görebilirsiniz — bu normaldir. Ama **komutları her zaman `(.venv)` aktifken çalıştırın.** Emin olmak için: `which python` çalıştırın, çıktı `.venv/bin/python` göstermeli (sisteminizin veya conda'nın Python'u değil).

**3. Paketi kurun:**

```bash
pip install -e ".[viz,notebook]"
```

Bu komut şunları kurar: `sympy`, `numpy`, `matplotlib`, `plotly`, `fastapi`, `uvicorn`, `antlr4-python3-runtime` ve diğer tüm bağımlılıklar. Tek komut, ayrıca bir şey kurmanız gerekmez.

> **`-e .` ne demek?** "Editable install" — paketi kurar ama dosyaları yerinde bırakır. Kodda değişiklik yaparsanız tekrar kurmanız gerekmez, değişiklikler anında yansır.

**4. Kurulumu doğrulayın:**

İki şeyi kontrol edin — Python paketi ve LaTeX parser:

```bash
# Python paketi çalışıyor mu?
python -c "from aot import TaylorExpansion; print('AOT hazir')"

# LaTeX parser çalışıyor mu? (antlr4 doğru kurulmuş mu?)
python -c "from sympy.parsing.latex import parse_latex; print(parse_latex(r'x^2 + y^2'))"
```

İlk komut `AOT hazir`, ikinci komut `x**2 + y**2` yazmalıdır.

Eğer ikinci komut hata veriyorsa (`antlr4` ile ilgili):
```bash
pip install antlr4-python3-runtime==4.11.1
```

**5. (Web arayüzü için) Frontend'i kurun:**

```bash
cd web && npm install && cd ..
```

---

## Çalıştırma

### Web Arayüzü (en kolay yol)

Python veya Jupyter bilmenize gerek yok. Tek komutla her şey başlar:

```bash
aot launch
```

Bu komut backend'i ve frontend'i başlatır, tarayıcınızı otomatik açar. Fonksiyonunuzu LaTeX ile yazın, açılım noktasını girin, "Hesapla" deyin.

Durdurmak için terminalde `Ctrl+C` basın.

> **Alternatif yollar** (aynı şeyi yapar):
> - Linux/Mac: `./start.sh`
> - Windows: `start.bat` dosyasına çift tıklayın
> - Make: `make launch`

### Sorun Giderme

**"Address already in use" hatası:**
Önceki bir çalıştırmadan kalan process var. Önce onu durdurun:
```bash
pkill -f uvicorn    # Linux/Mac
# veya
taskkill /f /im uvicorn.exe    # Windows
```
Sonra tekrar `aot launch` çalıştırın.

**"HTTP 500" veya "Matematiksel Hata" (web arayüzünde):**
Backend çalışmıyor olabilir. Ayrı bir terminalde şunu çalıştırıp hata mesajını kontrol edin:
```bash
source .venv/bin/activate
python -m uvicorn server.main:app --reload --port 8000
```

**"No module named uvicorn" hatası:**
Bağımlılıklar düzgün kurulmamış. Sanal ortamda olduğunuzdan emin olup tekrar kurun:
```bash
source .venv/bin/activate
pip install -e ".[viz,notebook]"
```

**LaTeX parser çalışmıyor (her fonksiyon hata veriyor):**
`antlr4` paketi eksik veya yanlış versiyonda:
```bash
pip install antlr4-python3-runtime==4.11.1
pkill -f uvicorn
python -m uvicorn server.main:app --reload --port 8000
```

**Conda ortamı karışıklığı:**
`which python` çalıştırın. Eğer `.venv/bin/python` yerine `/home/user/miniconda3/bin/python` gösteriyorsa, sanal ortam aktif değil:
```bash
source .venv/bin/activate
which python    # .venv/bin/python göstermeli
```

---

## Hızlı Başlangıç (Python API)

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

## Fonksiyon Galerisi

Aşağıdaki fonksiyonlar AOT'u keşfetmek için özenle seçilmiştir. Her birini web arayüzüne doğrudan yapıştırabilir, hem sembolik `(a_1, a_2)` hem sayısal noktalarda deneyebilirsiniz.

### Klasik Yüzeyler

Bu fonksiyonların şekilleri ikoniktir — matematiğin "manzara resimleri" gibi düşünün.

| LaTeX | Ne yaptığı | Deneyin |
|---|---|---|
| `e^{-(x_1^2 + x_2^2)}` | **Gaussian çan eğrisi.** Her yerde düzgün, Taylor'ın en rahat çalışacağı fonksiyon. | Sayısal: `(1, 0)` — tepenin yamacından bakın |
| `\sin(x_1) \cdot \sin(x_2)` | **Yumurta kartonu.** Periyodik dalgalı yüzey. Uzaklaştıkça Taylor tamamen sapar — bunu grafikte görmek öğretici. | Sayısal: `(0, 0)` |
| `\cos(x_1^2 + x_2^2)` | **Dairesel dalgalanma.** Suya taş atınca oluşan halkalar gibi. Radyal simetrisi var ama Taylor bunu kırar — ilginç sonuç. | Sayısal: `(0, 0)` |

### Kesirli & Rasyonel Fonksiyonlar

Türevleri elle almak acı verici — tam olarak AOT'un parladığı alan.

| LaTeX | Ne yaptığı | Deneyin |
|---|---|---|
| `\frac{1}{1 + x_1^2 + x_2^2}` | **2D Lorentzian.** Fizikte rezonans eğrisi, istatistikte Cauchy dağılımı. Orijinde güzel tepe. | Sembolik: `(a_1, a_2)` |
| `\frac{x_1 \cdot x_2}{x_1^2 + x_2^2 + 1}` | **Eyer noktası (saddle point).** Gradient sıfır ama ne minimum ne maksimum — Hessian'a bakarak bunu doğrulayın. | Sayısal: `(0, 0)` |
| `\frac{\sin(x_1 \cdot x_2)}{1 + x_1^2 + x_2^2}` | **Trigonometrik + rasyonel karışım.** El ile türev almak kabus olurdu. | Sembolik: `(a_1, a_2)` |

### Doğa Bilimleri & Fizik Motivasyonlu

Bu fonksiyonlar fiziksel anlam taşır — potansiyel alanları, dalga denklemleri ve harmonik fonksiyonlar.

| LaTeX | Ne yaptığı | Deneyin |
|---|---|---|
| `\ln(1 + x_1^2 + x_2^2)` | **Logaritmik potansiyel.** 2D elektrostatikte karşınıza çıkar. Orijinde düz, uzakta logaritmik büyüme. | Sayısal: `(0, 0)` |
| `\sqrt{x_1^2 + x_2^2 + 1}` | **Hiperboloid yüzey.** Karekök Taylor'ı zorlar; açılımdaki kesirleri inceleyin. | Sembolik: `(a_1, a_2)` |
| `e^{x_1} \cdot \cos(x_2)` | **Laplace denkleminin çözümü!** Harmonik fonksiyon. İpucu: Hessian'ın çapraz elemanlarının toplamı (iz/trace) sıfır olmalı — AOT ile kontrol edin. | Sembolik: `(a_1, a_2)` |

### Sembolik Açılımı "Vay Be" Dedirtecekler

Bu fonksiyonları `(a_1, a_2)` civarında el ile açmayı hayal edin — saatler sürer. AOT saniyeler içinde yapar.

| LaTeX | Ne yaptığı | Deneyin |
|---|---|---|
| `\frac{e^{x_1 \cdot x_2}}{\cos(x_1) + \cos(x_2) + 2}` | **AOT'un varoluş sebebi.** Hem sembolik hem sayısal `(0, 0)` ile deneyin ve karşılaştırın. | Sembolik: `(a_1, a_2)` sonra Sayısal: `(0, 0)` |
| `\arctan\left(\frac{x_2}{x_1}\right)` | **Polar açı fonksiyonu (θ).** Orijinde tanımsız ama `(1, 0)` civarında zarif bir açılım verir. | Sayısal: `(1, 0)` |
| `e^{x_2 \cdot \ln(x_1)}` | Bu aslında `x_1^{x_2}` demek. Üstel güç fonksiyonu — Taylor açılımı şaşırtıcı derecede karmaşık. | Sayısal: `(1, 1)` |

### 3 Değişkenli (R³ → R)

Bu fonksiyonlar için grafik çizilemez (4 boyut gerekir) ama sembolik açılımları çok zengin. Hessian 3×3 matris olarak gelir.

| LaTeX | Ne yaptığı | Deneyin |
|---|---|---|
| `e^{x_1 \cdot x_2 \cdot x_3}` | **Üçlü etkileşim terimi.** Hessian'daki çapraz türevlere dikkat edin — üç değişkenin birbirini nasıl etkilediğini gösterir. | Sembolik: `(a_1, a_2, a_3)` |
| `\frac{x_1 + x_2 + x_3}{1 + x_1^2 + x_2^2 + x_3^2}` | **3D rasyonel.** Sembolik açılımı uzun çıkar ama her terimi anlamlı. | Sayısal: `(1, 1, 1)` |
| `\sin(x_1 + x_2) \cdot e^{-x_3^2}` | **Dalga + sönümleme.** İki değişkende salınım, üçüncüde Gaussian sönümleme — fiziksel anlam taşır. | Sembolik: `(a_1, a_2, a_3)` |

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

## Proje Yapısı

```
aot/
├── aot/                   ← Ana Python paketi
│   ├── __init__.py        ← Dışarıya açılan API
│   ├── core.py            ← TaylorExpansion sınıfı (sembolik motor)
│   ├── numerical.py       ← lambdify ile sayısal değerlendirme
│   ├── visualization.py   ← Grafik çizim fonksiyonları
│   └── utils.py           ← Yardımcı fonksiyonlar
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
