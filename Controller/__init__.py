from threading import Thread

import test2
import teste



carrinho1 = Thread(target=test2.run)
carrinho2 = Thread(target=teste.run)


carrinho1.start()
carrinho2.start()
