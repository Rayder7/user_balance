# user_balance
ТЗ:
Разработать API для работы со балансом пользователя и перемещении денег между пользователями системы
У каждого пользователя есть свой баланс, изначально он равен 0.
Разработать API, который принимает число (количество копеек) и увеличивает баланс залогиненного пользователя на данное число. Абстрагируемся от реально оплаты и денег, реализуя лишь последний шаг зачисления денег на  баланс. Он может пополнить свой баланс в любой момент времени.
Разработать API, который производит списание с текущего баланса пользователя на баланс другого пользователя по user_id по требованию (перевод денег). Только залогиненный пользователь может производить списания со своего баланса, но начисления возможны без каких-либо подтверждений со  стороны получателя.
Разработать API, который возвращает текущий баланс залогиненого пользователя в рублях.

Дополнительные требования:
вести учет транзакций по операциям пополнения баланса
вести учет транзакций по операциям переводов между пользователями
запрещать переводы, если сумма перевода  для  инициатора превышает его  текущий баланс
предусмотреть случаи одновременного пополнения и списания денег в рамках одного пользователя (мне прислали 100 рублей и одновременно в ту же секунду/долю  секунды я положил 1 рубль- баланс должен быть 101, а не 100  или  1).

