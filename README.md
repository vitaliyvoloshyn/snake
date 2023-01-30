# snake
web framework

Для запуска сервера необходимо запустить на исполнение файл run.py. Сервер запускается на порту 8080

Урок 8.
- добавлены doc-string;
- добавлен файл Антипаттерны в коде.docx;

Урок 7.
- добавлена страница со списком студентов;
- добавлена страница детализации по студенту;
- реализованы дополнительные классы ListView и DetailView;
- реализована простая ORM для студентов на базе sqlite;
- файл БД создается при запуске приложения;
- возможности ORM: вставка, чтение, обновление, удаление данных из таблицы;
- для выборки есть три функции all - выборка всех записей из таблицы, find_by_id - выборка по id записи, filter - выборка по условию (принимает параметр и значение);

Урок 6.
- добавлены подкатегории;
- добавлена страница регистрации студентов;
- при изменении в курсе (на странице выведена кнопка информирования) студенты этого курса получают уведомление;
- на данный момент уведомления студенты получают по смс и электронной почте, есть возможность добавлять другие способы информирования;

Урок 5.
- добавлен декоратор AppRout для добавления связки url-view в приложение, чтобы можно было добавлять url-ы, как в фреймворке Flask @AppRout(‘/some_url/’);
- добавлен декоратор @debug, для view, если мы указываем данный декоратор над view, то в терминал выводятся название функции и время ее выполнения;

Урок 4.
- добавлена страница с категориями обучения;
- на странице с категориями автоматически создаются три категории;
- реализована возможность создавать новые категории прямо на странице;
- при переходе на выбранную категорию будет показан список доступных курсов в данной категории;
- пользователь имеет возможность создавать курсы и копировать уже созданные курсы;
- реализован простой логер на основе паттерна синглтон;
- если при создании нового логера указать имя уже существующего логера, то будет возвращен объект существующего логера, а если логеров с таким именем не создавалось, то вернется новый обьект логера;
- у логера есть два обработчика, которые выводят данные в консоль и в файл соответственно, по умолчанию у логера обработчик вывода в консоль;
- логирование происходит в методах get и post класса TemplateView, от которого наследуются пользовательские view;

Урок 3.
- главная страница разбита на несколько страниц - главная, о нас, контакты и т.д по меню - каждая ссылка меню теперь указывает на новую страницу;
- создана базовая страница (base.html), которая включает в себя меню из файла menu.html, и, которую наследуют остальные страницы;
- при прописывании ссылок на новые страницы (главная, о нас, контакты и т.д по меню) столкнулся с проблемой некорректного формирования итоговой ссылки для перехода (в href указывал относительные пути). Для решения проблемы при определении обьекта View в модуле main я добавил контекст ({'url': f'{environ["wsgi.url_scheme"]}://{environ["HTTP_HOST"]}'}), который передавался в шаблоны. Значение по данному ключу я и подставлял в href ({{ url }}/contact, {{ url }}/about и т.д.). Кажется костылем, но работает. В Django был тег url, а в Jinja такого не нашел.

Урок 2.
- доработана возможность обрабатывать post-запросы, которые отсылаются на сервер с помощью формы обратной связи на главной странице;
- данные с формы записываются в файл и отображаются в консоли;
- "сырые" данные в теле post-запроса парсятся с помощью функции parse-qs модуля urllib.parse

Урок 1.
- разработан базовый функционал фреймворка;
- фреймворк может принимать и обрабатывать get-запросы и query-string;
- на остальные запросы фреймворк отдает 405 ошибку;
- на данный момент фреймворк обрабатывает get-запросы по двум url - '' и '/developer' (ссылка находится в самом низу домашней страницы в разделе designed by), остальное - ошибка 404
- главная страница взята на одном из сайтов готовых html-шаблонов;
- в фреймворк интегрирован шаблонизатор jinja2;
- кроме HTML фреймворк умеет отдавать статические файлы (картинки, стили, js);
