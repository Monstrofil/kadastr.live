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
        <h1>Про проєкт</h1>
        <div>
          <div class="alert alert-danger">
            Увага! Останнє оновлення даних відбулось <b>16 лютого 2023 р. о 11:26</b>.
            Подальші оновлення не гарантуються через блокування
            <a href="http://wikimap.dzk.gov.ua/wiki/API_%D0%95-%D1%81%D0%B5%D1%80%D0%B2%D1%96%D1%81%D0%B8">API ДЗК</a>
            на час воєнного стану.<br>
            <br>
            <strong>Звертаємо також увагу на те, що сервіс не є офіційним джерелом та не має використовуватись у
              професійній діяльності.</strong>
          </div>
        </div>
        <p>
          Проект розроблено волонтером <a target="_blank" href="https://www.openstreetmap.org/">OpenStreetMap
          Ukraine</a> <b>без</b> участі Міністерства цифрової трансформації та іноземних партнерів. Подяка за підтримку
          кавомашині та домашньому коту.
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

    <div class="row" style="margin-bottom: 50px;">
      <div class="col-md-12">
        <h2>
          Підключення до сторонніх програм
        </h2>
        <p>
          Для підключення мапи до сторонніх програм доступні наступні сервіси:
        </p>
        <div class="row">
          <div class="col-xs-12 col-md-6">
            <div class="card w-100">
              <div class="card-body">
                <h5 class="card-title">WMTS</h5>
                <p class="card-text">
                  https://kadastr.live/tiles/raster/styles/parcels/wmts.xml
                </p>
              </div>
            </div>
          </div>
          <div class="col-xs-12 col-md-6">
            <div class="card w-100">
              <div class="card-body">
                <h5 class="card-title">XYZ</h5>
                <p class="card-text">
                  https://kadastr.live/tiles/raster/styles/parcels/{z}/{x}/{y}.png
                </p>
              </div>
            </div>
          </div>
        </div>
        <p>
          Публічні посилання доступні без авторизації усім бажаючим.
        </p>
      </div>
    </div>

     <div class="row">
      <div class="col-md-12">
        <h2>
          Контакти для зв'язку
        </h2>
        <div class="row">
          <div class="col-xs-12 col-md-6">
            <div class="card w-100">
              <div class="card-body">
                <h5 class="card-title">GitHub Issues</h5>
                <p class="card-text">
                  <a href="https://github.com/Monstrofil/kadastr.live/issues" target="_blank">
                    https://github.com/Monstrofil/kadastr.live/issues
                  </a>
                </p>
              </div>
            </div>
          </div>
          <div class="col-xs-12 col-md-6">
            <div class="card w-100">
              <div class="card-body">
                <h5 class="card-title">Telegram</h5>
                <p class="card-text">
                  <a href="https://t.me/Monstrofil" target="_blank">https://t.me/Monstrofil</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AboutPageComponent'
}
</script>
