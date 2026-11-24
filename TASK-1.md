# Задание 1. Поиск дефектов по скриншотам

> **Дисклеймер.** Все дефекты в отчёте предполагаемые. Анализ выполнен по трём статичным скриншотам без бизнес-требований, макетов и доступа к стенду. Заполненная форма редактирования принята за эталон значений по условию задания. Для подтверждения поведения, воспроизводимости и правил отображения нужно сверить требования и проверить сценарии на стенде. Приоритеты предварительные.

Проверка касается объявления № 52291995943. [Условие задания](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2026/QA-trainee-assignment-autumn-2026.md#задание-1)

**Приоритеты**

- **P0** - критический, основной сценарий заблокирован.
- **P1** - высокий, расхождение влияет на цену, способ получения или адрес сделки.
- **P2** - средний, искажены важные сведения или затруднено отдельное действие.
- **P3** - низкий, локальная проблема отображения или текста.

На фрагментах красная рамка выделяет наблюдение, зелёная - значение или область для сверки.

## Заполненная форма редактирования

[Оригинал скриншота](https://drive.google.com/file/d/1jVmZyPtSsMqVbkf_sQVX3e0bmNH0Ix18/view?usp=sharing)

<table>
<thead>
<tr>
  <th width="146">Дефект</th>
  <th width="24">P</th>
  <th width="238">Фактический и ожидаемый результат</th>
  <th width="395">Скриншоты</th>
</tr>
</thead>
<tbody>
<tr>
  <td valign="top">Дублируется заголовок "Внешний вид"</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> Над блоком "Фотографии" подряд отображаются два одинаковых заголовка "Внешний вид".</p><p><strong>Ожидание.</strong> У блока один заголовок "Внешний вид".</p></td>
  <td valign="top"><a href="./task-1-images/qa-f01.png"><img src="./task-1-images/qa-f01.png" width="400" alt="Заполненная форма редактирования - Дублируется заголовок &quot;Внешний вид&quot;"></a></td>
</tr>
<tr>
  <td valign="top">Углы главной фотографии выступают за синюю рамку</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> У миниатюры с меткой "Главная" за скруглённой рамкой видны прямые углы изображения. Это заметно в верхнем левом углу на увеличенном фрагменте.</p><p><strong>Ожидание.</strong> Углы миниатюры обрезаны по контуру рамки.</p></td>
  <td valign="top"><a href="./task-1-images/qa-photo-corners.png"><img src="./task-1-images/qa-photo-corners.png" width="400" alt="Миниатюра главной фотографии в форме"></a><br><a href="./task-1-images/qa-photo-corner-close.png"><img src="./task-1-images/qa-photo-corner-close.png" width="320" alt="Увеличенный верхний левый угол миниатюры"></a></td>
</tr>
</tbody>
</table>

## Карточка продавца

[Оригинал скриншота](https://drive.google.com/file/d/1sRxQqr7mOjBcX9uMJ18GMT52onD6Tz7O/view?usp=sharing)

<table>
<thead>
<tr>
  <th width="146">Дефект</th>
  <th width="24">P</th>
  <th width="238">Фактический и ожидаемый результат</th>
  <th width="395">Скриншоты</th>
</tr>
</thead>
<tbody>
<tr>
  <td valign="top">Подменено название объявления</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В заголовке "Диван прямой QA Sofa 2026 раскладной". В форме указано "угловой модульный".</p><p><strong>Ожидание.</strong> Заголовок совпадает с полем "Название" в форме и отображается полностью: "Диван угловой модульный QA Sofa 2026 раскладной".</p></td>
  <td valign="top"><a href="./task-1-images/qa-s01.png"><img src="./task-1-images/qa-s01.png" width="400" alt="Карточка продавца - Подменено название объявления"></a><br><a href="./task-1-images/qa-ref-title.png"><img src="./task-1-images/qa-ref-title.png" width="400" alt="Название в форме редактирования"></a></td>
</tr>
<tr>
  <td valign="top">На недельном графике нет данных при ненулевых просмотрах</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> На выбранной вкладке "Просмотры" показано 8. За период 10.08-16.08 на графике видны сетка и оси, значения по дням не отображаются.</p><p><strong>Ожидание.</strong> График показывает распределение просмотров за выбранную неделю. Итог совпадает со счётчиком за тот же период и по тем же правилам подсчёта.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s02.png"><img src="./task-1-images/qa-s02.png" width="400" alt="Карточка продавца - На недельном графике нет данных при ненулевых просмотрах"></a></td>
</tr>
<tr>
  <td valign="top">Метка "6" на оси графика смещена, под ней виден обрезанный символ</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> У линии 6 видны смещённая цифра и фрагмент второй метки. Остальные подписи расположены напротив своих линий.</p><p><strong>Ожидание.</strong> У каждой линии одна целая подпись, выровненная по линии.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s03.png"><img src="./task-1-images/qa-s03.png" width="354" alt="Карточка продавца - Метка &quot;6&quot; на оси графика смещена, под ней виден обрезанный символ"></a></td>
</tr>
<tr>
  <td valign="top">Текст "Просмотры 8" смещён вверх внутри плашки</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В блоке "Статистика за неделю" надпись "Просмотры 8" расположена примерно на 5 пикселей выше середины серой плашки.</p><p><strong>Ожидание.</strong> Надпись выровнена по вертикали внутри плашки.</p></td>
  <td valign="top"><a href="./task-1-images/qa-views-label.png"><img src="./task-1-images/qa-views-label.png" width="400" alt="Плашка просмотров в блоке недельной статистики"></a></td>
</tr>
<tr>
  <td valign="top">Главная фотография оказалась второй в галерее</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Первой выбрана фотография с поднятой деревянной панелью слева. Кадр с выдвинутым нижним ящиком стоит вторым, хотя в форме он отмечен как главный.</p><p><strong>Ожидание.</strong> Фотография с меткой "Главная" расположена первой и открывается при первоначальном показе карточки.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s04.png"><img src="./task-1-images/qa-s04.png" width="400" alt="Карточка продавца - Главная фотография оказалась второй в галерее"></a><br><a href="./task-1-images/qa-ref-photo.png"><img src="./task-1-images/qa-ref-photo.png" width="400" alt="Фотография с меткой &quot;Главная&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">В описание добавлен текст, которого нет в форме</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> К предложению про угловой раскладной диван добавлено "с ящиком для белья, подлокотниками и подушками".</p><p><strong>Ожидание.</strong> Блок "Описание" передаёт текст из формы. Последнее предложение - "Угловой раскладной диван."</p></td>
  <td valign="top"><a href="./task-1-images/qa-s05.png"><img src="./task-1-images/qa-s05.png" width="400" alt="Карточка продавца - В описание добавлен текст, которого нет в форме"></a><br><a href="./task-1-images/qa-ref-desc.png"><img src="./task-1-images/qa-ref-desc.png" width="400" alt="Исходный текст описания в форме"></a></td>
</tr>
<tr>
  <td valign="top">В тексте акции использована форма "2,5 раз"</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> На плашке "Скидка на доставку" написано "До 2,5 раз больше шансов на продажу".</p><p><strong>Ожидание.</strong> На плашке написано "До 2,5 раза больше шансов на продажу". После десятичной дроби используется форма "раза".</p></td>
  <td valign="top"><a href="./task-1-images/qa-delivery-copy.png"><img src="./task-1-images/qa-delivery-copy.png" width="400" alt="Текст на плашке скидки на доставку"></a></td>
</tr>
<tr>
  <td valign="top">В заголовке акции виден технический идентификатор</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> На плашке отображается "Скидки в test_sale_ops".</p><p><strong>Ожидание.</strong> В заголовке отображается пользовательское название акции.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s06.png"><img src="./task-1-images/qa-s06.png" width="354" alt="Карточка продавца - В заголовке акции виден технический идентификатор"></a></td>
</tr>
<tr>
  <td valign="top">Иконка на плашке со скидкой не отрисовалась</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В верхней части плашки "Скидки в test_sale_ops" виден значок недоступного изображения.</p><p><strong>Ожидание.</strong> Отображается иконка акции или предусмотренное оформление на случай отсутствия изображения.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s07.png"><img src="./task-1-images/qa-s07.png" width="354" alt="Карточка продавца - Иконка на плашке со скидкой не отрисовалась"></a></td>
</tr>
<tr>
  <td valign="top">Нижняя часть страницы повторяет верхнюю панель навигации</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> Под блоком "Распродажа" видны те же пункты "Для бизнеса", "Карьера в Авито", "Ещё" и "Разместить объявление", что в шапке. <em>Требует уточнения, где возник повтор.</em></p><p><strong>Ожидание.</strong> Верхняя панель отображается в предусмотренном месте. Для подтверждения повтора на странице нужно сверить её на стенде и проверить, как сделан длинный снимок.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s08.png"><img src="./task-1-images/qa-s08.png" width="400" alt="Карточка продавца - Нижняя часть страницы повторяет верхнюю панель навигации"></a><br><a href="./task-1-images/qa-ref-seller-header.png"><img src="./task-1-images/qa-ref-seller-header.png" width="400" alt="Панель навигации вверху карточки продавца"></a></td>
</tr>
<tr>
  <td valign="top">Под раскрытыми заголовками нет содержимого</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> У блоков "Похожие объявления" и "Распродажа" стрелки направлены вверх, под обоими заголовками пусто. <em>Требует уточнения состояния блоков.</em></p><p><strong>Ожидание.</strong> Если стрелка вверх означает, что блок раскрыт, видны элементы или сообщение об их отсутствии. Блок без данных можно скрыть, если так предусмотрено дизайном.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s09.png"><img src="./task-1-images/qa-s09.png" width="400" alt="Карточка продавца - Под раскрытыми заголовками нет содержимого"></a></td>
</tr>
<tr>
  <td valign="top">В характеристиках отсутствуют модель и цвет производителя</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В форме заполнены "Модель" и "Цвет от производителя". Этих строк в блоке "Характеристики" нет. Модель читается в заголовке объявления. <em>Требует уточнения состава блока.</em></p><p><strong>Ожидание.</strong> Если характеристики включают эти поля, в них отображаются "QA Sofa 2026" и "Графит".</p></td>
  <td valign="top"><a href="./task-1-images/qa-s10.png"><img src="./task-1-images/qa-s10.png" width="400" alt="Карточка продавца - В характеристиках отсутствуют модель и цвет производителя"></a><br><a href="./task-1-images/qa-ref-model-color.png"><img src="./task-1-images/qa-ref-model-color.png" width="382" alt="Поля &quot;Модель&quot; и &quot;Цвет от производителя&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">Источник значений в поле "Особенности" неочевиден</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке перечислены ящик для белья, подлокотники и подушки. В показанной форме отдельного поля "Особенности" нет. <em>Требует уточнения источника данных.</em></p><p><strong>Ожидание.</strong> Если блок заполняется данными объявления, он показывает только указанные продавцом значения или значения из согласованного источника.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s11.png"><img src="./task-1-images/qa-s11.png" width="377" alt="Карточка продавца - Источник значений в поле &quot;Особенности&quot; неочевиден"></a></td>
</tr>
<tr>
  <td valign="top">В блоке о товаре отсутствует отметка "Б/у"</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В форме выбрано "Б/у". В блоке "О диване" отображается только общее состояние "Отличное". <em>Требует уточнения правил отображения.</em></p><p><strong>Ожидание.</strong> Если карточка показывает оба признака, "Б/у" и "Отличное" отображаются как два отдельных значения.</p></td>
  <td valign="top"><a href="./task-1-images/qa-s12.png"><img src="./task-1-images/qa-s12.png" width="400" alt="Карточка продавца - В блоке о товаре отсутствует отметка &quot;Б/у&quot;"></a><br><a href="./task-1-images/qa-ref-used.png"><img src="./task-1-images/qa-ref-used.png" width="334" alt="Выбранное состояние &quot;Б/у&quot; в форме"></a></td>
</tr>
</tbody>
</table>

## Карточка товара

[Оригинал скриншота](https://drive.google.com/file/d/1mSG2furdRm9aLjt7tWKSXaD5iaWXyzgQ/view?usp=sharing)

<table>
<thead>
<tr>
  <th width="146">Дефект</th>
  <th width="24">P</th>
  <th width="238">Фактический и ожидаемый результат</th>
  <th width="395">Скриншоты</th>
</tr>
</thead>
<tbody>
<tr>
  <td valign="top">Цена завышена на 27 000 ₽</td>
  <td align="center" valign="top">P1</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке указано 52 000 ₽.</p><p><strong>Ожидание.</strong> В карточке указано 25 000 ₽, как в форме редактирования.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i01.png"><img src="./task-1-images/qa-i01.png" width="350" alt="Карточка товара - Цена завышена на 27 000 ₽"></a><br><a href="./task-1-images/qa-ref-price.png"><img src="./task-1-images/qa-ref-price.png" width="400" alt="Цена 25 000 руб. в форме"></a></td>
</tr>
<tr>
  <td valign="top">Карточка сообщает, что продавец отключил включённую доставку</td>
  <td align="center" valign="top">P1</td>
  <td valign="top"><p><strong>Факт.</strong> Блок показывает "Доставка недоступна" и пояснение "Продавец отключил доставку для объявления". В форме доставка включена, выбраны два способа отправки.</p><p><strong>Ожидание.</strong> Карточка учитывает включённую доставку. Если она недоступна по другим условиям, блок показывает фактическую причину.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i02.png"><img src="./task-1-images/qa-i02.png" width="400" alt="Карточка товара - Карточка сообщает, что продавец отключил включённую доставку"></a><br><a href="./task-1-images/qa-ref-delivery.png"><img src="./task-1-images/qa-ref-delivery.png" width="345" alt="Включённая доставка и два способа отправки в форме"></a></td>
</tr>
<tr>
  <td valign="top">В адресе указан неправильный номер дома</td>
  <td align="center" valign="top">P1</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке "Москва, пл. Революции, 5".</p><p><strong>Ожидание.</strong> В карточке "Москва, пл. Революции, 3", как в форме.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i03.png"><img src="./task-1-images/qa-i03.png" width="400" alt="Карточка товара - В адресе указан неправильный номер дома"></a><br><a href="./task-1-images/qa-ref-place.png"><img src="./task-1-images/qa-ref-place.png" width="400" alt="Адрес с номером дома 3 в форме"></a></td>
</tr>
<tr>
  <td valign="top">Завышено количество товара в наличии</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Рядом со статусом указано "в наличии 3 шт.".</p><p><strong>Ожидание.</strong> Количество соответствует форме: "в наличии 1 шт.".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i04.png"><img src="./task-1-images/qa-i04.png" width="350" alt="Карточка товара - Завышено количество товара в наличии"></a><br><a href="./task-1-images/qa-ref-qty.png"><img src="./task-1-images/qa-ref-qty.png" width="376" alt="Количество 1 шт. в форме"></a></td>
</tr>
<tr>
  <td valign="top">Главная фотография оказалась второй в галерее</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Первой выбрана фотография с поднятой деревянной панелью слева. Кадр с выдвинутым нижним ящиком стоит вторым. Аналогичное наблюдение в карточке продавца.</p><p><strong>Ожидание.</strong> Фотография с меткой "Главная" расположена первой и открывается при первоначальном показе карточки.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i05.png"><img src="./task-1-images/qa-i05.png" width="400" alt="Карточка товара - Главная фотография оказалась второй в галерее"></a><br><a href="./task-1-images/qa-ref-photo.png"><img src="./task-1-images/qa-ref-photo.png" width="400" alt="Фотография с меткой &quot;Главная&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">Характеристика "Форма" противоречит заголовку и форме редактирования</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В характеристиках "Форма: Прямой" и "Угол: Универсальный". В заголовке товар назван угловым.</p><p><strong>Ожидание.</strong> В характеристиках "Форма: Угловой". Значение "Универсальный" в поле "Угол" сохраняется.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i06.png"><img src="./task-1-images/qa-i06.png" width="400" alt="Карточка товара - Характеристика &quot;Форма&quot; противоречит заголовку и форме редактирования"></a><br><a href="./task-1-images/qa-ref-shape.png"><img src="./task-1-images/qa-ref-shape.png" width="337" alt="Угловая форма и универсальный угол в форме"></a></td>
</tr>
<tr>
  <td valign="top">Модульный диван помечен как немодульный</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В характеристиках "Модульный: Нет". В заголовке диван назван модульным.</p><p><strong>Ожидание.</strong> В характеристиках "Модульный: Да", как в форме.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i07.png"><img src="./task-1-images/qa-i07.png" width="400" alt="Карточка товара - Модульный диван помечен как немодульный"></a><br><a href="./task-1-images/qa-ref-modular.png"><img src="./task-1-images/qa-ref-modular.png" width="218" alt="Выбранное значение &quot;Да&quot; в поле &quot;Модульный&quot;"></a></td>
</tr>
<tr>
  <td valign="top">Карточка отрицает наличие спального места и указывает его размер</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В характеристиках "Спальное место: Нет" и "Размер спального места: 140 × 200 см".</p><p><strong>Ожидание.</strong> В характеристиках "Спальное место: Есть" и размер 140 × 200 см, как в форме.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i08.png"><img src="./task-1-images/qa-i08.png" width="400" alt="Карточка товара - Карточка отрицает наличие спального места и указывает его размер"></a><br><a href="./task-1-images/qa-ref-bed.png"><img src="./task-1-images/qa-ref-bed.png" width="400" alt="Спальное место и размеры 140 × 200 см в форме"></a></td>
</tr>
<tr>
  <td valign="top">Карточка отрицает наличие раскладного механизма и указывает его тип</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В характеристиках "Раскладной механизм: Нет", в соседней колонке "Тип механизма: Еврокнижка".</p><p><strong>Ожидание.</strong> В характеристиках "Раскладной механизм: Есть", тип - "Еврокнижка".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i09.png"><img src="./task-1-images/qa-i09.png" width="400" alt="Карточка товара - Карточка отрицает наличие раскладного механизма и указывает его тип"></a><br><a href="./task-1-images/qa-ref-mechanism.png"><img src="./task-1-images/qa-ref-mechanism.png" width="392" alt="Наличие механизма и тип &quot;Еврокнижка&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">Высота и глубина поменялись местами</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Высота - 95 см, глубина - 85 см.</p><p><strong>Ожидание.</strong> Высота - 85 см, глубина - 95 см. Значение каждой величины соответствует своему полю в форме.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i10.png"><img src="./task-1-images/qa-i10.png" width="381" alt="Карточка товара - Высота и глубина поменялись местами"></a><br><a href="./task-1-images/qa-ref-size.png"><img src="./task-1-images/qa-ref-size.png" width="400" alt="Глубина 95 см и высота 85 см в форме"></a></td>
</tr>
<tr>
  <td valign="top">Обивка ошибочно отмечена как требующая замены</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В блоке "О диване" указано "Состояние обивки: Требует замены".</p><p><strong>Ожидание.</strong> Отображается "Состояние обивки: Всё в порядке".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i11.png"><img src="./task-1-images/qa-i11.png" width="400" alt="Карточка товара - Обивка ошибочно отмечена как требующая замены"></a><br><a href="./task-1-images/qa-ref-upholstery.png"><img src="./task-1-images/qa-ref-upholstery.png" width="388" alt="Состояние обивки в форме"></a></td>
</tr>
<tr>
  <td valign="top">Раскладной механизм ошибочно отмечен как требующий ремонта</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В блоке "О диване" указано "Раскладной механизм: Требуется ремонт".</p><p><strong>Ожидание.</strong> Отображается "Раскладной механизм: Всё в порядке".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i12.png"><img src="./task-1-images/qa-i12.png" width="400" alt="Карточка товара - Раскладной механизм ошибочно отмечен как требующий ремонта"></a><br><a href="./task-1-images/qa-ref-condition-mechanism.png"><img src="./task-1-images/qa-ref-condition-mechanism.png" width="399" alt="Состояние раскладного механизма в форме"></a></td>
</tr>
<tr>
  <td valign="top">Каркас ошибочно отмечен как требующий ремонта</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> В блоке "О диване" указано "Каркас: Требуется ремонт".</p><p><strong>Ожидание.</strong> Отображается "Каркас: Всё в порядке".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i13.png"><img src="./task-1-images/qa-i13.png" width="400" alt="Карточка товара - Каркас ошибочно отмечен как требующий ремонта"></a><br><a href="./task-1-images/qa-ref-frame.png"><img src="./task-1-images/qa-ref-frame.png" width="301" alt="Состояние каркаса в форме"></a></td>
</tr>
<tr>
  <td valign="top">В заголовке "Описание" срезан верх буквы "О"</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке товара верхний контур буквы "О" обрезан. В карточке продавца та же буква в заголовке видна целиком.</p><p><strong>Ожидание.</strong> Заголовок отображается целиком, включая верхний контур буквы "О".</p></td>
  <td valign="top"><a href="./task-1-images/qa-description-heading.png"><img src="./task-1-images/qa-description-heading.png" width="383" alt="Обрезанный верх буквы О в карточке товара"></a><br><a href="./task-1-images/qa-ref-description-heading.png"><img src="./task-1-images/qa-ref-description-heading.png" width="383" alt="Целая буква О в карточке продавца"></a></td>
</tr>
<tr>
  <td valign="top">В описание добавлен текст, которого нет в форме</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> К предложению про диван дописано "с ящиком для белья, подлокотниками и подушками". Аналогичное наблюдение в карточке продавца.</p><p><strong>Ожидание.</strong> Блок "Описание" показывает текст из формы. Последнее предложение - "Угловой раскладной диван."</p></td>
  <td valign="top"><a href="./task-1-images/qa-i14.png"><img src="./task-1-images/qa-i14.png" width="400" alt="Карточка товара - В описание добавлен текст, которого нет в форме"></a><br><a href="./task-1-images/qa-ref-desc.png"><img src="./task-1-images/qa-ref-desc.png" width="400" alt="Исходный текст описания в форме"></a></td>
</tr>
<tr>
  <td valign="top">В карточке покупателя показана общая подпись вместо имени продавца</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> На карточке товара продавец подписан "Пользователь", в карточке продавца - "Гедеоныч". <em>Требует уточнения правил для гостя.</em></p><p><strong>Ожидание.</strong> Если имя публично для гостя, в карточке отображается "Гедеоныч".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i15.png"><img src="./task-1-images/qa-i15.png" width="400" alt="Карточка товара - В карточке покупателя показана общая подпись вместо имени продавца"></a><br><a href="./task-1-images/qa-ref-seller.png"><img src="./task-1-images/qa-ref-seller.png" width="356" alt="Имя в карточке продавца"></a></td>
</tr>
<tr>
  <td valign="top">Статус объявления расходится между карточками</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Карточка товара показывает "Опубликовано". В карточке продавца объявления № 52291995943 указано "На проверке". <em>Требует сверки времени и правил модерации.</em></p><p><strong>Ожидание.</strong> При одновременной проверке обе карточки отражают актуальное состояние объявления. Если изменения проходят модерацию при доступной опубликованной версии, статус продавца поясняет, что проверяется новая версия.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i16.png"><img src="./task-1-images/qa-i16.png" width="350" alt="Карточка товара - Статус объявления расходится между карточками"></a><br><a href="./task-1-images/qa-ref-status.png"><img src="./task-1-images/qa-ref-status.png" width="400" alt="Статус и номер объявления в карточке продавца"></a></td>
</tr>
<tr>
  <td valign="top">Публичный счётчик просмотров показывает ноль при ненулевой статистике продавца</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> У объявления № 52291995943 указано "0 просмотров (+0 сегодня)". В статистике продавца за 10.08-16.08 - 8 просмотров. <em>Требует сверки правил подсчёта и времени обновления.</em></p><p><strong>Ожидание.</strong> При одинаковых правилах подсчёта и синхронных данных общий счётчик учитывает просмотры за прошедшую часть этой недели.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i17.png"><img src="./task-1-images/qa-i17.png" width="400" alt="Карточка товара - Публичный счётчик просмотров показывает ноль при ненулевой статистике продавца"></a><br><a href="./task-1-images/qa-ref-views.png"><img src="./task-1-images/qa-ref-views.png" width="400" alt="Номер объявления, неделя и число просмотров в карточке продавца"></a></td>
</tr>
<tr>
  <td valign="top">Подсказка предлагает спросить о доставке, которая помечена как недоступная</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> Под полем вопроса есть кнопка "Отправите Авито Доставкой?". Выше та же карточка сообщает, что продавец отключил доставку. <em>Требует уточнения логики подсказок.</em></p><p><strong>Ожидание.</strong> Если подсказки зависят от доступных способов получения, вопрос о доставке появляется при релевантном для него состоянии.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i19.png"><img src="./task-1-images/qa-i19.png" width="400" alt="Карточка товара - Подсказка предлагает спросить о доставке, которая помечена как недоступная"></a><br><a href="./task-1-images/qa-i02.png"><img src="./task-1-images/qa-i02.png" width="400" alt="Плашка недоступной доставки в той же карточке"></a></td>
</tr>
<tr>
  <td valign="top">У баннера "Найти своё на ресейле" отсутствует иллюстрация</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В правом нижнем углу баннера видны значок недоступного изображения и текст "Ресейл".</p><p><strong>Ожидание.</strong> Баннер показывает иллюстрацию или предусмотренное оформление на случай её отсутствия.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i20.png"><img src="./task-1-images/qa-i20.png" width="400" alt="Карточка товара - У баннера &quot;Найти своё на ресейле&quot; отсутствует иллюстрация"></a></td>
</tr>
<tr>
  <td valign="top">После подвала повторяется верхняя панель навигации</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> Под ссылками подвала снова видны верхнее меню, логотип и начало поисковой строки. <em>Требует уточнения, где возник повтор.</em></p><p><strong>Ожидание.</strong> Верхняя панель отображается в предусмотренном месте. Для подтверждения повтора на странице нужно сверить её на стенде и проверить, как сделан длинный снимок.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i21.png"><img src="./task-1-images/qa-i21.png" width="400" alt="Карточка товара - После подвала повторяется верхняя панель навигации"></a><br><a href="./task-1-images/qa-ref-item-header.png"><img src="./task-1-images/qa-ref-item-header.png" width="400" alt="Панель навигации вверху карточки товара"></a></td>
</tr>
<tr>
  <td valign="top">В характеристиках отсутствуют модель и цвет производителя</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В блоке есть "Основной цвет: Серый". Строк с моделью и цветом от производителя нет. Модель читается в заголовке объявления. <em>Требует уточнения состава блока.</em></p><p><strong>Ожидание.</strong> Если характеристики включают эти поля, в них отображаются "QA Sofa 2026" и "Графит".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i22.png"><img src="./task-1-images/qa-i22.png" width="400" alt="Карточка товара - В характеристиках отсутствуют модель и цвет производителя"></a><br><a href="./task-1-images/qa-ref-model-color.png"><img src="./task-1-images/qa-ref-model-color.png" width="382" alt="Поля &quot;Модель&quot; и &quot;Цвет от производителя&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">Источник значений в поле "Особенности" неочевиден</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке перечислены ящик для белья, подлокотники и подушки. В показанной форме отдельного поля "Особенности" нет. Такое же наблюдение в карточке продавца. <em>Требует уточнения источника данных.</em></p><p><strong>Ожидание.</strong> Если блок заполняется данными объявления, он показывает только указанные продавцом значения или значения из согласованного источника.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i23.png"><img src="./task-1-images/qa-i23.png" width="400" alt="Карточка товара - Источник значений в поле &quot;Особенности&quot; неочевиден"></a></td>
</tr>
<tr>
  <td valign="top">В блоке о товаре отсутствует отметка "Б/у"</td>
  <td align="center" valign="top">P2</td>
  <td valign="top"><p><strong>Факт.</strong> Покупатель видит "Состояние: Отличное", а выбранное в форме "Б/у" в блоке отсутствует. <em>Требует уточнения правил отображения.</em></p><p><strong>Ожидание.</strong> Если оба признака предназначены для покупателя, карточка показывает "Б/у" и отдельно общее состояние "Отличное".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i24.png"><img src="./task-1-images/qa-i24.png" width="400" alt="Карточка товара - В блоке о товаре отсутствует отметка &quot;Б/у&quot;"></a><br><a href="./task-1-images/qa-ref-used.png"><img src="./task-1-images/qa-ref-used.png" width="334" alt="Выбранное состояние &quot;Б/у&quot; в форме"></a></td>
</tr>
<tr>
  <td valign="top">В нижней ссылке лишняя заглавная буква</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> Рядом с подвалом ссылка "Модульные Диваны в Москве".</p><p><strong>Ожидание.</strong> В ссылке "Модульные диваны в Москве".</p></td>
  <td valign="top"><a href="./task-1-images/qa-i25.png"><img src="./task-1-images/qa-i25.png" width="400" alt="Карточка товара - В нижней ссылке лишняя заглавная буква"></a></td>
</tr>
<tr>
  <td valign="top">В цене увеличен интервал перед символом рубля</td>
  <td align="center" valign="top">P3</td>
  <td valign="top"><p><strong>Факт.</strong> В карточке товара между суммой и символом ₽ заметно больше места, чем в аналогичном ценовом блоке карточки продавца. <em>Требует сверки с макетом.</em></p><p><strong>Ожидание.</strong> Сумма и обозначение валюты оформлены единообразно по правилам отображения цены.</p></td>
  <td valign="top"><a href="./task-1-images/qa-i26.png"><img src="./task-1-images/qa-i26.png" width="297" alt="Карточка товара - В цене увеличен интервал перед символом рубля"></a><br><a href="./task-1-images/qa-ref-seller-price.png"><img src="./task-1-images/qa-ref-seller-price.png" width="289" alt="Написание цены в карточке продавца"></a></td>
</tr>
</tbody>
</table>
