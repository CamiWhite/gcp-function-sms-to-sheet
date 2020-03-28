import main

class TestMain:

  def test_extract_details(self):
    message = 'BancoX le informa Pago por $10,000.00 a FABRICA DE JUGUETES SA desde cta *1111. 11/11/1111 11:11. Inquietudes al 0345109095/018000931987.'
    (reference, cost) =  main.extract_details(message)
    assert reference == 'FABRICA DE JUGUETES SA'
    assert cost == 10000

  def test_extract_details_alternative(self):
    message = 'BancoX le informa Compra por $50.000,00 en RAPPI PMZ 11:11. 11/11/1111 T.Cred *1111. Inquietudes al 0345109095/018000931987.'
    (reference, cost) =  main.extract_details(message)
    assert reference == 'RAPPI PMZ'
    assert cost == 50000