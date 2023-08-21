<template>
  <template v-if="config && styleLoaded">
    <template
        v-for="directory in config"
        :key="directory.id">
      <LayerDirectory :directory="directory" :map="map"/>
    </template>
  </template>


</template>

<script>
import LayerDirectory from "@/components/map/controls/filterControls/LayerDirectory";

export default {
  name: "MapFilter",
  components: {LayerDirectory},
  props: {
    map: null
  },
  data() {
    return {
      config: [],
      styleLoaded: false
    }
  },
  mounted() {
    function mapLoaded() {
      this.styleLoaded = true;
    }
    this.map.on('styledata', mapLoaded.bind(this));

    this.config = [
      {
        id: "base-layers",
        name: "Базові шари",
        collapsed: false,
        groups: [
          {
            name: "Фонові зображення",
            layers: [
              {
                id: "orto-tiles",
                name: "Ортофото ДЗК (2011)",
                hidden: false,
                checked: false
              },
              {
                id: "topo-tiles",
                name: "Топографія (ДНІГК)",
                hidden: false,
                checked: false
              },
              //{
              //  id: "orto-ersi",
              //  name: "Ортофото ESRI (2018+)",
              //  hidden: false,
              //  checked: false
              //},
              {
                id: "openstreetmap",
                name: "OpenStreetMap",
                hidden: false,
                checked: true
              },
              // {
              //   id: "dzk",
              //   name: "WMS шар ДЗК",
              //   hidden: false,
              //   checked: false
              // },
            ]
          }
        ],

      },
      {
        id: "dzk__pzf",
        name: "Векторні дані",
        collapsed: false,
        groups: [
          {
            name: "Земельний кадастр",
            layers: [
              {
                id: "dzk__index_map_lines",
                chain: "dzk__index_map_poly",
                name: "Індексна карта",
                hidden: false,
                checked: false
              },
              {
                id: "land_polygones",
                name: "Геометрія ділянок",
                hidden: false,
                checked: true,
                metadata: {
                  filterSchema: {
                    "ownership": {
                      type: "select",
                      hint: "Форма власності",
                      options: [
                        {
                          id: "Державна власність",
                          name: "Державна власність",
                          checked: true
                        },
                        {
                          id: "Комунальна власність",
                          name: "Комунальна власність",
                          checked: true
                        },
                        {
                          id: "Приватна власність",
                          name: "Приватна власність",
                          checked: true
                        },
                        {
                          id: "Не визначено",
                          name: "Не визначено",
                          customFilter: ["any", ["==", ["get", "ownership"], ""], ["==", ["get", "ownership"], "Не визначено"]],
                          checked: true
                        }
                      ]
                    }
                    ,
                    "category": {
                      type: "select",
                      hint: "Категорія земель",
                      options: [
                        {
                          id: "Землі водного фонду",
                          name: "Водний фонд",
                          checked: true
                        },
                        {
                          id: "Землі житлової та громадської забудови",
                          name: "Житлова та громадська забудова",
                          checked: true
                        },
                        {
                          id: "Землі історико-культурного призначення",
                          name: "Історико-культурні ділянки",
                          checked: true
                        },
                        {
                          id: "Землі лісогосподарського призначення",
                          name: "Лісове господарство",
                          checked: true
                        },
                        {
                          id: "Землі оздоровчого призначення",
                          name: "Оздоровчого призначення",
                          checked: true
                        },
                        {
                          id: "Землі природно-заповідного та іншого природоохоронного призначення",
                          name: "Природоохоронного призначення",
                          checked: true
                        },
                        {
                          id: "Землі промисловості, транспорту, зв’язку, енергетики, оборони та іншого призначення",
                          name: "Промисловості, транспорту, оборони",
                          checked: true
                        },
                        {
                          id: "Землі рекреаційного призначення",
                          name: "Рекреаційного призначення",
                          checked: true
                        },
                        {
                          id: "Землі сільськогосподарського призначення",
                          name: "Сільськогосподарського призначення",
                          checked: true
                        },
                        {
                          id: "Не визначено",
                          name: "Інше",
                          customFilter: ["any", ["==", ["get", "category"], ""], ["==", ["get", "category"], "Не визначено"]],
                          checked: true
                        },
                      ]
                    }
                  },
                  lazyLoading: true
                }
              },
            ]
          },
          {
            name: "Довкілля",
            layers: [
              {
                id: "dzk__pzf",
                name: "Заповідний фонд",
                hidden: false,
                checked: false
              },
              {
                id: "nsdi_sm_merega",
                name: "Смарагдова мережа",
                hidden: false,
                checked: false
              },
              {
                id: "water_lines_other",
                chain: ["water_lines_middle_rivers", "water_lines_large", "water_lines_text"],
                name: "Річкова мережа",
                hidden: false,
                checked: false
              },
              {
                id: "river_basin",
                name: "Басейни річок",
                hidden: false,
                checked: false
              },
              {
                id: "river_subbasin",
                name: "Суббасейни річок",
                hidden: false,
                checked: false
              },
              {
                id: "manage_parcel",
                name: "Межі водогосподарств",
                hidden: false,
                checked: false
              },
            ]
          },
          {
            name: "Адміністративний устрій",
            layers: [
              {
                id: "dzk__atu_oblast",
                // chain: "dzk__atu_oblast__text",
                name: "Межі областей",
                hidden: false,
                checked: false
              },
              {
                id: "dzk__atu_rayon",
                chain: "dzk__atu_rayon__text",
                name: "Межі районів",
                hidden: false,
                checked: false
              },
              {
                id: "dzk__atu_terhromad__line",
                chain: "dzk__atu_terhromad__text",
                name: "Межі громад",
                hidden: false,
                checked: false
              }
            ]
          }
        ]
      },

    ]

  }
}
</script>

