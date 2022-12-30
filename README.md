<h1>Запуск приложения через docker</h1>

<h3>Создание образа</h3>
<code>docker build -t api-car .</code>
</br>
<h3>Запуск контейнера с приложением</h3>
<code>docker run -p 5000:5000 api-car</code>
</br>
<h3>Страница документации</h3>
<code>http://127.0.0.1:5000/swagger-ui</code>
</br>
<h4>Сайт с данными</h4>
<code>https://www.mentoday.ru/technics/garage/ot-model-t-do-model-3-100-samyh-vazhnyh-avtomobiley-v-istorii-chelovechestva/</code>