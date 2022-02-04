/***
 * TODO
 * [ ] ADD ALL EXTERNAL FUNCTIONS AS IMPORTS DOM HELPERS AND MBX HELPERS
 * [ ] ADD NUMBER NEXT TO LAYER GROUP OR LAYER DIRECTORY SHOWING HOW MANY LAYERS ARE TURNED ON
 * [ ] ADD MORE DOCS
 * [ ] ADD ZOOM LEVEL VISIBILITY ON TOGGLES MAKE INACTIVE ON ZOOMEND ADD FUNCTION TO CHECK FOR VISIBILITY
 */

import * as domHelper from "mapbox-layer-control/lib/domHelpers.js";
import * as mglHelper from "mapbox-layer-control/lib/mglHelpers.js";

export class layerControlGrouped {

  constructor(options) {
    options = (!options) ? {} : options;

    this._collapsed = false;

    if ((options.options && options.options.collapsed) || (options && options.collapsed)) {
      this._collapsed = true;
    }

    if ((options.options && options.options.addLayers)) {
      this._addLayers = true;
    }

    this._layers = options.layers.reverse().slice()
    this._layerIds = this._layers.reduce((i,l) => {
      return [...i, l.id]
    }, [])
    
    let directories = [];
    let groups = [];

    directories = this._layers.reduce(function (i, layer) {
      return [...i, layer.directory]
    }, []);

    this._directories = [...new Set(directories)];

    groups = this._layers.reduce(function (i, layer) {
      if (!layer.group) layer.group = "Operational Layers"
      return [...i, layer.group]
    }, []);

    this._groups = [...new Set(groups)];

    let config = {};

    this._directories.forEach(function (d) {
      options.layers.forEach(function (layer) {
        if (layer.directory === d) {
          config[layer.directory] = {}
        }
      })
    })

    this._layers.forEach(function (l) {
      if (!l.group) l.group = "Operational Layers";
      config[l.directory][l.group] = []
    })

    this._layers.forEach(function (l) {
      config[l.directory][l.group].push(l)
    });

    let layersClone = this._layers.slice();

    //CREATE A LAYERS GROUP IN METADATA FOR FILTERING
    this._layers.forEach(function (l) {
      if (!l.name) l.name = l.id
      //ADD METADATA AND METADATA.LAYERS IF NOT EXIST
      if (!l.metadata) {
        l.metadata = {};
      }
      if (!l.metadata.layers) l.metadata.layers = [l.id];

      //ADD CHILD LAYERS IF ANY
      if (l.children) {
        layersClone.forEach(child => {
          if (child.parent && child.parent === l.id) l.metadata.layers = [...l.metadata.layers, child.id]
        })
      }
    })

    this._layerControlConfig = config

    // this._layers.forEach(l => {
    //   Object.keys(l).map(k => {
    //     l.metadata[k] = l[k]
    //   })
    // })

    console.log(config)

    // TARGET CONFIG LAYOUT
    // this._layerControlConfig = {
    //     directory1: {
    //       groupName: [
    //         {
    //           id: "id",
    //           name: "name",
    //           legend: "html"
    //         }
    //       ]
    //     },
    //     directory2: {
    //       groupName: [
    //         {
    //           id: "id",
    //           name: "name",
    //           legend: "html"
    //         }
    //       ]
    //     }
    //   }
  }

  onAdd(map) {

    this._map = map;
    let _this = this;
    this._sources = []; //only add the lazyLoading source information to one layer

    this._container = map.getContainer();

    // SETUP MAIN MAPBOX CONTROL
    this._div = lcCreateButton(this._collapsed);

    // GET THE MAP LAYERS AND LAYER IDS AND SET TO VISIBLE ANY LAYER IDS IN THE QUERY PARAMS, AND ADD THEM TO THE QUERY PARAMS IF MISSING
    const activeLayers = mglHelper.GetActiveLayers(this._map, this._layers);

    this._layers.forEach(l => {

      // CHECK TO MAKE SURE ALL CHILDREN ARE ACTIVE IF PARENT IS ACTIVE
      if (l.parent && activeLayers.includes(l.parent)) {
        map.setLayoutProperty(l.id, "visibility", "visible");
        lcSetActiveLayers(l.id, true)
      }

      //NO ORPHANED CHILDREN
      if (l.parent && activeLayers.includes(l.id) && !activeLayers.includes(l.parent)) {
        map.setLayoutProperty(l.id, "visibility", "none");
        map.setLayoutProperty(l.parent, "visibility", "none");
        lcSetActiveLayers(l.id, false)
      }
    })

    this._activeLayers = mglHelper.GetActiveLayers(this._map, this._layers)
    this._mapLayers = this._map.getStyle().layers;
    this._mapLayerIds = mglHelper.GetMapLayerIds(this._mapLayers);

    // console.log(this._mapLayerIds, this._layers)

    //BUILD DIRECTORIES, GROUPS, LAYER TOGGLES AND LEGENDS FROM THE layerControlConfig
    for (let d in this._layerControlConfig) {

      //CREATE DIRECTORY
      let directory = d;

      let layerCount = 0;

      this._layers.forEach(l => {
        if (l.directory === d && !l.parent) {
          var checked = mglHelper.GetLayerVisibility(this._mapLayers, this._mapLayerIds, l.id);
          if (checked) {
            layerCount = layerCount + 1
          }
        }
      })

      let directoryDiv = lcCreateDicrectory(directory, layerCount);
      directoryDiv.classList.add("collapsed");

      //CREATE TOGGLE GROUPS
      for (let g in this._layerControlConfig[d]) {

        let groupDiv = lcCreateGroup(g, this._layerControlConfig[d][g], map)

        let groupLayers = this._layerControlConfig[d][g];

        // CREATE INDIVIDUAL LAYER TOGGLES
        for (let l = 0; l < groupLayers.length; l++) {
          let layer = groupLayers[l];
          let style = mglHelper.GetStyle(this._mapLayers, layer);
          if (!layer.legend && style) {
            layer.simpleLegend = lcCreateLegend(style)
          }
          let checked;
          checked = mglHelper.GetLayerVisibility(this._mapLayers, this._mapLayerIds, layer.id);
          // if (layer.parent) {
          //   checked = mglHelper.GetLayerVisibility(this._mapLayers, this._mapLayerIds, layer.parent);
          // }
          let { layerSelector, newSources } = lcCreateLayerToggle(this._map, layer, checked, this._sources);
          this._sources = newSources;
          groupDiv.appendChild(layerSelector)
        }
        directoryDiv.appendChild(groupDiv);
      }

      this._div.appendChild(directoryDiv)
    }

    /****
     * ADD EVENT LISTENERS FOR THE LAYER CONTROL ALL ON THE CONTROL ITSELF
     ****/
    if (this._collapsed) {
      this._div.addEventListener("mouseenter", function (e) {
        setTimeout(function () {
          e.target.classList.remove("collapsed")
        }, 0)
        return
      });
  
      this._div.addEventListener("mouseleave", function (e) {
        e.target.classList.add("collapsed")
        return
      });
    }

    this._div.addEventListener("click", function (e) {
      // console.log(e.target);

      if (e.target.dataset.layerControl) {
        e.target.classList.remove("collapsed");
        return
      }

      if (e.target.className === "checkbox") {
        e.target.children[0].click();
        // e.target.blur()
        return
      }

      if (e.target.dataset.mapLayer) {
        mglHelper.SetLayerVisibility(map, e.target.checked, e.target.id);
        if (e.target.dataset.children) {
          let children = document.querySelectorAll("[data-parent]");
          for (let i = 0; i < children.length; i++) {
            if (children[i].dataset.parent === e.target.id) {
              children[i].click()
            }
          }
        }
      // e.target.blur()              
        return
      }

      if (e.target.dataset.mapFilter) {
        console.log('Filter toggled', e.target.dataset)
        console.log(map.getLayer(e.target.dataset.mapLayerName))
        console.log(map.getLayer(e.target.dataset.mapLayerName).setFilter)

        let allMapFilters = ["all"];

        let allFilters = document.querySelectorAll("[data-map-filter]");
        const groupedMap = Array.from(allFilters).reduce(
            (entryMap, e) => entryMap.set(e.dataset.group, [...entryMap.get(e.dataset.group)||[], e]),
            new Map()
        );
        groupedMap.forEach((filters, key) => {
          console.log("key, filters", key, filters)
          let valueFilters = ["any"];
          Array.from(filters).forEach((filter) => {
            console.log(filter)
            if (!filter.checked)
              return

            valueFilters.push(JSON.parse(filter.dataset.filterQuery));
          })
          console.log(valueFilters);
          allMapFilters.push(valueFilters);
        })
        console.log(groupedMap)

        map.setFilter(e.target.dataset.mapLayerName, allMapFilters);
        console.log(allMapFilters);

      //   mglHelper.SetLayerVisibility(map, e.target.checked, e.target.id);
      //   if (e.target.dataset.children) {
      //     let children = document.querySelectorAll("[data-parent]");
      //     for (let i = 0; i < children.length; i++) {
      //       if (children[i].dataset.parent === e.target.id) {
      //         children[i].click()
      //       }
      //     }
      //   }
      // // e.target.blur()
        return
      }

      if (e.target.dataset.mapLayer && e.target.dataset.group != false) {
        e.stopPropagation();
        let group = e.target.dataset.group;
        let groupMembers = document.querySelectorAll("[data-group]");
        for (let i = 0; i < groupMembers.length; i++) {
          if (group != "false" && groupMembers[i].dataset.group === group) {
            mglHelper.SetLayerVisibility(map, e.target.checked, groupMembers[i].id);
          }
        }
        return
      }

      if (e.target.dataset.layergroup) {
        // console.log("layergroup")
        let inputs = e.target.parentElement.querySelectorAll("[data-master-layer]");
        // CHECK IF ANY OF THE BOXES ARE NOT CHECKED AND IF NOT THEM CHECK THEM ALL
        if (!domHelper.GetAllChecked(inputs)) {
          for (let i = 0; i < inputs.length; i++) {
            if (!inputs[i].checked) {
              inputs[i].click()
            }
          }
        }
        // IF ALL OF THE BOXES ARE CHECKED, UNCHECK THEM ALL
        else {
          for (let i = 0; i < inputs.length; i++) {
            let checkbox = inputs[i];
            if (checkbox.checked) {
              checkbox.click()
            }
          }
        }
        return
      }

      if (e.target.dataset.directoryToggle) {
        if (e.target.parentElement.children[2].style.display != "none") {
          e.target.parentElement.children[0].className = "collapsed"
        } else {
          e.target.parentElement.children[0].className = ""
        }
        domHelper.ToggleChildren(e.target.parentElement, 2)

        setTimeout(function() {
          if (!isScrolledIntoView(e.target.parentElement)) {
            window.location.hash = e.target.id;
          }
        },410);
        setTimeout(function() {
          _this._map.resize()
        },450)
        return
      }
    })

    if (this._collapsed) {
      this._map.on("click", function () {
        _this._div.classList.add("collapsed")
      })
    }

    //NEED TO SET THIS AT THE BEGINNING PASS IN CURRENT ZOOM OF MAP AND SET DISABLED PROPERTY THIS ALSO BINGS IN WEIRD THINGS WITH THE CHECK ALL GROUP BUT TACKLE THAT LATER
    this._map.on("zoomend", function () {
      let zoomendMap = this;
      let lcLayers = document.querySelectorAll("[data-master-layer]");
      lcLayers.forEach(function (l) {
        if (l.dataset.minzoom && l.dataset.minzoom > zoomendMap.getZoom()) {
          l.parentElement.style.opacity = "0.3"
          l.disabled = true
        } else {
          l.parentElement.style.opacity = "1"
          l.disabled = false
        }
      });
    })

    return this._div;
  }

  onRemove(map) {
    this._map = map;
    this._div.parentNode.removeChild(this._div);
    this._map = undefined;
  }
}

/****
 * HELPER FUNCTIONS
 ****/

function lcCreateFilterToggle(map, option, checked, sources, group, mapLayerName) {
  let div = document.createElement("div");
  div.className = "checkbox";
  div.title = "Map Layer";

  let input = document.createElement("input");
  input.name = option.name;
  input.type = "checkbox";
  input.id =  option.id;
  input.dataset.group = group;

  input.className = "layer slide-toggle";
  input.dataset.mapLayerName = mapLayerName;
  input.dataset.mapFilter = true;
  console.log(option.customFilter)
  if(option.customFilter) {
    input.dataset.filterQuery = JSON.stringify(option.customFilter)
  }
  else {
    input.dataset.filterQuery = JSON.stringify([
        "==", ["get", group],
      option.id]);
  }

  if (checked) input.checked = true;

  let label = document.createElement("label");
  label.setAttribute("for", option.id);

  label.innerText = option.name;
  label.dataset.layerToggle = "true";

  div.appendChild(input);
  div.appendChild(label);

  return { layerSelector: div, newSources: sources }
}

function lcCreateLayerToggle(map, layer, checked, sources) {
  let div = document.createElement("div");
  div.className = "checkbox";
  div.title = "Map Layer";

  if (layer.hidden) {
    div.style.display = "none";
    div.dataset.hidden = true
  }

  let input = document.createElement("input");
  input.name = (!layer.name) ? layer.id : layer.name;
  input.type = "checkbox"
  input.id = layer.id;
  input.dataset.group = (layer.group) ? layer.group : false;

  if (layer.metadata.lazyLoading && layer.metadata.source && layer.metadata.source.id && layer.metadata.source.type && layer.metadata.source.data) {
    //only add the source to one layer to avoid loading the same file simultaneously - not really working...need to do this per layer group
    // if (!sources.includes()) {
      // console.log("adding lazy loading info for", layer.id)
      input.dataset.lazyLoading = true;
      input.dataset.source = layer.metadata.source.id
      input.dataset.sourceType = layer.metadata.source.type
      input.dataset.sourceData = layer.metadata.source.data
      sources.push(layer.metadata.source.id)
    // }
  }

  if (layer.minzoom) {
    input.dataset.minzoom = layer.minzoom
  }

  if (layer.children) {
    input.dataset.children = true;
    input.dataset.masterLayer = true;
  }
  if (layer.parent) {
    input.dataset.parent = layer.parent;
  } else {
    input.dataset.masterLayer = true;
  }

  input.className = "layer slide-toggle";
  input.dataset.mapLayer = true;
  if (checked) input.checked = true;

  lcCheckLazyLoading(map, input);

  input.onclick = function () {
    lcCheckLazyLoading(map, this)
    lcSetActiveLayers(this.id, this.checked)
    lcSetLegendVisibility(this)
    lcSetDirectoryLayerCount(this);
  };

  let label = document.createElement("label");
  label.setAttribute("for", layer.id);
  let legend = document.createElement("div");
  if (layer.legend) {
    label.innerText = (!layer.name) ? layer.id : layer.name;
    legend.innerHTML = layer.legend;
    legend.className = "mgl-layerControlLegend";
    legend.dataset.layerChildLegend = "true"
    if (!checked) {
      legend.style.display = "none"
    }
  } else if (layer.simpleLegend) {
    label.innerHTML += layer.simpleLegend;
    label.innerHTML += (!layer.name) ? layer.id : layer.name;
    label.className = "mgl-layerControlLegend"
  } else {
    label.innerText = (!layer.name) ? layer.id : layer.name;
  }
  label.dataset.layerToggle = "true";

  div.appendChild(input);
  div.appendChild(label);

  if (layer.metadata && layer.metadata.filterSchema) {
    let filterSpan = document.createElement("span");
    filterSpan.style.float = "right";
    filterSpan.style.height = "20px";
    filterSpan.style.opacity = 0.3;
    filterSpan.innerHTML = filterIcon();
    filterSpan.onclick = function() {
      filterModal(map, layer)
    }
    filterSpan.onmouseenter = function() {
      this.style.opacity = 1;
    }
    filterSpan.onmouseleave= function() {
      this.style.opacity = 0.3;
    }

    let directory = lcCreateDicrectory("Фільтри", '-');
    directory.style = 'margin-left: 0;'

    // CREATE INDIVIDUAL FILTER TOGGLES
    for (const [key, value] of Object.entries(layer.metadata.filterSchema)) {

      let groupDiv = lcCreateGroup(value.hint, null, null);
      for (const option of Object.values(value.options)) {
        console.log(option)
        let { layerSelector, newSources } = lcCreateFilterToggle(
            map, option, checked, sources, key, layer.id);
          console.log(newSources)
         groupDiv.appendChild(layerSelector)
      }
      directory.appendChild(groupDiv)
      groupDiv.style.display = "none";
    }
    div.appendChild(directory)

    // collapse element by default
    div.children[0].classList.add("collapsed")
  }

  div.appendChild(legend);

  return { layerSelector: div, newSources: sources }
}

function lcCheckLazyLoading(map, layer) {
  if (layer.dataset.lazyLoading && layer.checked && !layer.dataset.sourceLoaded) {
    const source = map.getSource(layer.dataset.source);
    if (!source) return
    //not sure if using this internal property is the best way to check for this information
    //if multiple layers are using the same data, we could be fetching data as another data is also being fetched
    //maybe keep an internal variable of sources loaded to not load the same souce twice
    if (!source._data.features.length) {
      const loading = loadingIcon(map)
      fetch(layer.dataset.sourceData, {
        cache: "force-cache"
      })
      .then(res => res.json())
      .then(data => {
        //CHECK SOURCE AGAIN
        const newSource = map.getSource(layer.dataset.source);
        if ((newSource._data.features && !newSource._data.features.length) || (newSource._data.geometries && !newSource._data.geometries.length)) {
          map.getSource(layer.dataset.source).setData(data);
        }
        loading.style.display = "none";
        loading.remove();
        layer.setAttribute('data-source-loaded', true)
      })
    }
  }
}

function lcSetDirectoryLayerCount(e) {
  let targetDirectory = e.closest(".mgl-layerControlDirectory")
  let targetChildren = targetDirectory.querySelectorAll("[data-master-layer]");
  let targetCount = 0;
  targetChildren.forEach(function (c) {
    if (c.checked) targetCount = targetCount + 1;
  })
  if (targetCount > 0) {
    targetDirectory.children[1].children[0].innerHTML = targetCount;
    targetDirectory.children[1].children[0].style.display = "block"
  } else {
    targetDirectory.children[1].children[0].style.display = "none"
  }
}

function lcCreateDicrectory(directoryName, layerCount) {

  let accordian = document.createElement("div");
  accordian.dataset.accordian = true;
  accordian.style.backgroundColor = "white";
  accordian.className = "mgl-layerControlDirectory";

  let button = document.createElement("button");
  button.dataset.directoryToggle = true

  accordian.appendChild(button);

  let d = document.createElement("div");
  d.className = "directory"
  d.id = directoryName.replace(/ /g, "_");
  d.innerText = directoryName;
  d.dataset.name = directoryName;
  d.dataset.directoryToggle = true

  var counter = document.createElement("span");
  counter.style.background = "#0d84b3";
  counter.className = "mgl-layerControlDirectoryCounter";
  counter.style.display = (layerCount === 0) ? "none" : "block";
  counter.innerText = (!layerCount) ? "" : layerCount
  counter.style.float = "right";
  counter.style.color = "white";
  counter.style.padding = "1px 4px 0";
  d.appendChild(counter)

  accordian.appendChild(d);
  return accordian;
}

function lcCreateGroup(group, layers, map) {
  console.debug(layers, map)
  let titleInputChecked = false;
  // GET CHECKED STATUS OF LAYER GROUP
  // for (let i = 0; i < layers.length; i++) {
  //   let l = layers[i];
  //   console.log(l)
  //   if(map.getLayoutProperty(l.id, "visibility") === "visible") {
  //     titleInputChecked = true
  //     continue
  //   }else{
  //     break
  //   }
  // }

  let titleInputContainer = document.createElement("div");
  titleInputContainer.style.margin = "4px 0 4px 8px"

  let titleInput = document.createElement("input");
  titleInput.type = "checkbox";
  let titleInputId = "layerGroup_" + group.replace(/ /g, "_");
  titleInput.id = titleInputId;
  titleInput.style.display = "none";
  titleInput.dataset.layergroup = group;

  if (titleInputChecked) titleInput.checked = true

  let titleInputLabel = document.createElement("label");
  titleInputLabel.setAttribute("for", titleInputId);
  titleInputLabel.className = "mgl-layerControlGroupHeading"
  titleInputLabel.textContent = group;

  // let titleSettings = document.createElement("span");
  // titleSettings.style.position = "absolute";
  // titleSettings.style.right = "5px";
  // titleSettings.style.opacity = "0.8";
  // titleSettings.innerHTML = "<img src='https://icongr.am/material/dots-vertical.svg' height='24px'></img>"
  // titleInputLabel.appendChild(titleSettings);

  titleInputContainer.appendChild(titleInput);
  titleInputContainer.appendChild(titleInputLabel);

  return titleInputContainer;

}

function lcCreateButton(collapsed) {
  let div = document.createElement('div');
  div["aria-label"] = "Layer Control";
  div.dataset.layerControl = "true"
  div.className = 'mapboxgl-ctrl mapboxgl-ctrl-group mgl-layerControl';
  if (collapsed) div.classList.add("collapsed");

  let breadcrumb = document.createElement('div');
  breadcrumb.style = "text-align: center;\n" +
      "    background: white;\n" +
      "    border: 1px solid rgb(0 0 0 / 10%);\n" +
      "    border-right: 0;";
  breadcrumb.className = 'mgl-breadcrumb';
  breadcrumb.innerHTML = '<i style="font-size: 30px;\n' +
      '    line-height: 50px;" class="fa fa-map-o"></i>';

  const collapsedStyle = 'hiddenRight';
  breadcrumb.addEventListener('click', function () {
    if(div.classList.contains(collapsedStyle)) {
      div.classList.remove(collapsedStyle)
    }
    else {
      div.classList.add(collapsedStyle)
    }
  })
  div.classList.add(collapsedStyle)
  div.appendChild(breadcrumb)

  return div
}

function lcCreateLegend(style) {
  let type = Object.keys(style)
  let legend = false;
  if (type.indexOf("line-color") > -1 && isString(style["line-color"])) {
    legend = `<icon class='fa fa-minus' style='color:${style["line-color"]};margin-right:6px;'></icon>`;
  }
  if (type.indexOf("fill-color") > -1 && isString(style["fill-color"])) {
    legend = `<icon class='fa fa-square' style='color:${style["fill-color"]};margin-right:6px;'></icon>`;
  }
  if (type.indexOf("circle-color") > -1 && isString(style["circle-color"])) {
    legend = `<icon class='fa fa-circle' style='color:${style["circle-color"]};margin-right:6px;'></icon>`;
  }

  return legend
}

function isString(value) {
  return typeof value === 'string' || value instanceof String;
}

function lcSetActiveLayers(l, checked) {
  let _layer = l;
  let _visibility = checked;
  let params = new URLSearchParams(window.location.search);

  if (_visibility) {
    params.set(_layer, true);
    if (history.replaceState) {
      let url = window.location.protocol + "//" + window.location.host + window.location.pathname + "?" + params.toString() + window.location.hash;
      window.history.replaceState({
        path: url
      }, '', url);
    }
  } else {
    params.delete(_layer);
    if (history.replaceState) {
      let url = window.location.protocol + "//" + window.location.host + window.location.pathname + "?" + params.toString() + window.location.hash;
      window.history.replaceState({
        path: url
      }, '', url);
    }
  }
}

function lcSetLegendVisibility(e) {
  let _legend = e.parentElement.querySelectorAll("[data-layer-child-legend]");
  let _display = (!e.checked) ? "none" : "block";
  for (let i = 0; i < _legend.length; i++) {
    _legend[i].style.display = _display
  }
}

function filterModal(map, layer) {
  var id = layer.id + "_FilterModal";
  if (!document.getElementById(id)) {
    var modal = document.createElement("div");
    modal.id = id;
    modal.classList = "modal"
    modal.style.alignItems = "flex-start";
    modal.innerHTML = `
    <a href="#close" class="modal-overlay" aria-label="Close" style="opacity: 0.8"></a>
    <div class="modal-container" style="width: 400px;">
      <div class="modal-header">
        <a href="#close" class="btn btn-clear float-right modal-close" aria-label="Close"></a>
        <div class="modal-title h4">
          <span>Filter ${layer.name}</span>
        </div>
      </div>
      <div class="modal-body">
      </div>
      <div class="modal-footer">
      </div>
    </div>`

    var form = document.createElement("form");
    form.innerHTML = `
      ${createFormFields(layer.metadata.filterSchema)}
      <br>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button class="btn btn-outline" type="reset" style="float:right">Reset</button>
    `
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      window.location.hash = "#";
      var filter = buildFilter(new FormData(form), layer);
      console.log(filter)
      if (!filter) {
        layer.metadata.layers.forEach(l => {
          map.setFilter(l)
        })
      }else{
        layer.metadata.layers.forEach(l => {
          map.setFilter(l, filter)
        })
      }
    });

    form.addEventListener("reset", function() {
      layer.metadata.layers.forEach(l => {
        map.setFilter(l)
      })
    })

    modal.querySelector(".modal-body").appendChild(form)
    document.body.appendChild(modal);
    window.location.hash = "#"
    window.location.hash = id
  }else{
    window.location.hash = "#"
    window.location.hash = id
  }
}

function buildFilter(data, layer) {
  const fields = [...data.keys()];
  const values = [...data.values()];

  // console.log(fields, values)

  var filter = [];

  for (var i = 0; i < fields.length; i++) {
    if (fields[i].includes("operator")) continue;
    if (!values[i]) continue;
    let filterValue = values[i];
    if (layer.metadata.filterSchema[fields[i]].type === "date" && layer.metadata.filterSchema[fields[i]].epoch) {
      filterValue = new Date(filterValue + "T00:00:00").getTime();
      // console.log(filterValue, new Date(filterValue))
    }
    console.log(filterValue);
    //TODO ADD LOGIC FOR WHEN USING MULTIPLE IN SELECT OPTIONS - SHOULD BE ANOTHER ARRAY WITH 'IN' OPERATOR THEN THE == OPERATOR
    //MAYBE IF fields[i] === fields[i-1] then assume the multiple operator and use that, else do what we are currently doing
    switch (layer.metadata.filterSchema[fields[i]].type) {
      case "date" : filter.push([values[i + 1], ["get", fields[i] ], filterValue]); break;
      case "number" : filter.push([values[i + 1], ["get", fields[i] ], Number(filterValue) ]); break;
      default: filter.push(["==", ["get", fields[i]], filterValue]);
    }    
  }

  if (filter.length < 1) {
    return null
  }else{
    return ["all", ...filter]
  }
}

function createFormFields(schema) {
  let html = "";
  for (let s in schema) {
    let name = s.replace(/_/g, " ").toUpperCase()
    html += `
    <div class="form-group">
      <label class="form-label" for="${s}">${name}</label>
      ${(!schema[s].options) 
          ?
        `<input class="form-input" id="${s}" type="${schema[s].type}" name="${s}"  ${(!schema[s].readonly) ? '' : 'readonly="true"'} ${(!schema[s].required) ? '' : 'required="true"'}>`
          :
        `<select id="${s}" class="form-select" name="${s}" ${(!schema[s].required) ? '' : 'required="true"'}>
          ${schema[s].options.map(o => {
            return `<option>${o}</option>`
          })}
         </select>`
      }
      ${(!schema[s].hint) ? "" : `<p class="form-input-hint">${schema[s].hint}</p>`}
    </div>
    `

    if (schema[s].type === "date" || schema[s].type === "number") html += `
      <div class="form-group">
        <label  class="form-label" for="${s}_operator">${name} OPERATOR</label>
        <select id="${s}_operator"  name="${s}_operator" class="form-select">
          <option>></option>
          <option>>=</option>
          <option>==</option>
          <option><=</option>
          <option><</option>
        </select>
      </div>
    `

  }
  return html
}

function filterIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><path d="M0,0h24 M24,24H0" fill="none"/><path d="M4.25,5.61C6.27,8.2,10,13,10,13v6c0,0.55,0.45,1,1,1h2c0.55,0,1-0.45,1-1v-6c0,0,3.72-4.8,5.74-7.39 C20.25,4.95,19.78,4,18.95,4H5.04C4.21,4,3.74,4.95,4.25,5.61z"/><path d="M0,0h24v24H0V0z" fill="none"/></g></svg>`
}

function loadingIcon(map) {
  const svg = `<svg version="1.1" id="L9" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
    viewBox="0 0 100 100" enable-background="new 0 0 0 0" xml:space="preserve">
      <path fill="#fff" d="M73,50c0-12.7-10.3-23-23-23S27,37.3,27,50 M30.9,50c0-10.5,8.5-19.1,19.1-19.1S69.1,39.5,69.1,50">
        <animateTransform 
          attributeName="transform" 
          attributeType="XML" 
          type="rotate"
          dur="0.6s" 
          from="0 50 50"
          to="360 50 50" 
          repeatCount="indefinite" />
    </path>
  </svg>`
  const background = document.createElement("div");
  background.style.position = "absolute";
  background.style.top = 0;
  background.style.left = 0;
  background.style.bottom = 0;
  background.style.zIndex = 1;
  background.style.width = "100%"
  background.style.background = "rgba(255,255,255,0.5)"

  let div = document.createElement("div");
  div.innerHTML = svg;
  div.style.position = "absolute"
  div.style.display = "block";
  div.style.top = "50%";
  div.style.left = "50%";
  div.style.width = "120px";
  div.style.height = "120px";
  div.style.transform = "translate(-50%, -50%)";
  background.appendChild(div)
  map.getContainer().appendChild(background);

  return background
}

function isScrolledIntoView(el) {
  var rect = el.getBoundingClientRect();
  var elemTop = rect.top;
  var elemBottom = rect.bottom;
  var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight);
  // Partially visible elements return true:
  //isVisible = elemTop < window.innerHeight && elemBottom >= 0;
  return isVisible;
}