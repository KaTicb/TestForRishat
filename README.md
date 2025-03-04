# TestForRishat
[Ссылка на deploy версию](http://77.239.125.171/item/)

Иногда может тормозить, поэтому не нужно пугаться) 

P.S. тормозит обычно из-за загруженности сервера, тк я его использую для телеграм бота.

## Creds для админки
<b>login:</b> admin

<b>password:</b> AdminPass

## Окружение
Все ключи спрятаны в файле .env и подгружаются через dotenv библиотеку. Этот файл находится в .gitingore, поэтому его не будет в исходниках задания.
БД использовал SQLite, поэтому файл с базой тоже в .gitignore.

## Запуск
Если нужно локально запустить проект с продовой версией настроек, то нужно удалить файл "base/local_settings.py". Если локальную версию, то оставить все как есть.

```bash
git clone https://github.com/KaTicb/TestForRishat.git

cd TestForRishat

docker compose build
docker compose up -d

docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --no-input --clear
```
## Attention!
В дополнительном задании про использование "Stripe Payment Intent", я решил реализовать этот подход только для модели Item, потому что задание для бекендера и я решил не писать js для подтверждения, поэтому этот подход остался на уровне отправки json'a с secret_key. Для модели Order я оставил сессию для наглядности (ну и потому что так красивее :), чем голый апи респонс ).  
