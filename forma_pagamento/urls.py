from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_formas_pagamento, name='listar_formas_pagamento'),
    path('forma_pagamento/criar/', views.criar_forma_pagamento, name='criar_forma_pagamento'),
    path('forma_pagamento/editar/<int:id_forma_pagamento>/', views.editar_forma_pagamento, name='editar_forma_pagamento'),
    path('forma_pagamento/excluir/<int:id_forma_pagamento>/', views.excluir_forma_pagamento, name='excluir_forma_pagamento'),
]
