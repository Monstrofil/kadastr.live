<template>
  <div class="breadcrumbs">
    <div class="container">
      <ul>
        <li>
          <router-link to="/">Головна</router-link>
        </li>
        <li>
          <router-link active-class="active" to="/about">Про проєкт</router-link>
        </li>
      </ul>
    </div>
  </div>
  <div class="container text-block">
    <div class="row" style="margin-bottom: 50px;">
      <div class="col-md-12">
        <h1>About</h1>
        <div>
          <div class="alert alert-danger">
            Увага! Останнє оновлення даних відбулось <b>19 лютого 2022 р. о 21:14</b>.
            Подальші оновлення неможливі через блокування
            <a href="http://wikimap.dzk.gov.ua/wiki/API_%D0%95-%D1%81%D0%B5%D1%80%D0%B2%D1%96%D1%81%D0%B8">API ДЗК</a>
            на час воєнного стану.<br>
            <br>
            <strong>Звертаємо також увагу на те, що сервіс не є офіційним джерелом та не має використовуватись у професійній діяльності.</strong>
          </div>
        </div>
        <p>
          Проект розроблено волонтером <a target="_blank" href="https://www.openstreetmap.org/">OpenStreetMap
          Ukraine</a> <b>без</b> участі Міністерства цифрової трансформації та іноземних партнерів. Подяка за підтримку кавомашині та домашньому коту.
        </p>

        <p>
          Початковою метою проекту було створення бази даних поштових адрес земельних ділянок в межах України,
          що дало б поштовх до внесення адрес до навігаторів, електронних мап, тощо. Використання проекту в
          якості публічної кадастрової мапи є побічним ефектом та не підтримується авторами
          (капайте активніше на мі́зки керівництву ДЗК якщо вам така мапа потрібна).
        </p>

        <p>
          На даний момент проект оновлюється лише за наявності натхнення у його власника.
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h2>
          Підключення до сторонніх програм
        </h2>
        <p>
          Для підключення мапи до сторонніх програм доступні наступні сервіси:
        </p>
        <p>
          WMTS
          <pre>
https://kadastr.live/tiles/styles/kmplus/wmts.xml
          </pre>
        </p>
        <p>
          XYZ
          <pre>
https://kadastr.live/tiles/raster/styles/parcels/{z}/{x}/{y}.png
          </pre>
        </p>
        <p>
          Публічні посилання доступні без авторизації усім бажаючим.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AboutPageComponent'
}
</script>
