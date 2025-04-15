from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pagamentos, name='listar_pagamentos'),
    path('criar/', views.criar_pagamento, name='criar_pagamento'),
    path('editar/<int:id_pagamento>/', views.editar_pagamento, name='editar_pagamento'),
    path('excluir/<int:id_pagamento>/', views.excluir_pagamento, name='excluir_pagamento'),
    path('visualizar/<int:id_pagamento>/', views.visualizar_pagamento, name='visualizar_pagamento'),

]
