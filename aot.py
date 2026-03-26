import sympy as sp

# f:R^n --> R : f(x1,x2) = e^{x1^2+x2^2} ifadesini 'a' noktasında açalım
# 1. sembol tanıtımı;
x1, x2 = sp.symbols('x1 x2')
a1, a2 = sp.symbols('a1 a2')


# 2. fonksiyon tanıtımı
f = sp.exp(x1**2 + x2**2)

# 3. vektörleri tanımla
X = sp.Matrix([x1, x2]) # 2x1 sütun vektör!
A = sp.Matrix([a1, a2]) # 2x1 sütun vektör!

# 4. açılımdaki ifadeleri tanımla
diff        = X - A # (x-a) verir
grad_f      = sp.derive_by_array(f, (x1, x2)) # \nabla f(x) yani gradient verir
hess_f      = sp.hessian(f, (x1, x2)) # hessian verir
f_a         = f.subs({x1: a1, x2: a2}) # f_a demek f(a) demek artık
grad_f_a    = grad_f.subs({x1: a1, x2: a2}) # grad_f_a demek \nabla f(a) demek
hess_f_a    = hess_f.subs({x1: a1, x2: a2})
grad_matrix = sp.Matrix(grad_f_a)
hess_matrix = sp.Matrix(hess_f_a)



# 5. ifadeler ile oluşan terimleri belirle
# 5.1 f(a) ilk terim
term1 = f_a

# 5.2 \nabla^Tf(a)(x-a) ikinci terim
term2 = grad_matrix.dot(diff)

# 5.3 1/2 (x-a)^T * H(f(a)) * (x-a)
term3 = sp.Rational(1, 2) * (diff.T * hess_matrix * diff)[0] # sondaki [0] term3 sonucu oluşan 1x1 vektörün içindeki değeri al demek

# 6. Taylor açılımını toplam ifadesi
taylor = term1 + term2 + term3

# 6.1 Sadeleştirmeyi dene
simplified_taylor = sp.simplify(taylor)

# 7. Sonuçları yazdır
print(sp.latex(simplified_taylor)) # sonucu latex olarak verir