class Converter {
  constructor(data) {
    this.units = data.units;    // array of tuples (id, string), where id is same as index
    this.conv = data.conv;      // array of conv factors indexed by id
  }

  convert(value, fromUnit, toUnit) {
    return value * this.conv[toUnit] / this.conv[fromUnit];
  }

  toString(unit) {
    return this.units[unit][1];
  }
}

export var ingredientColours = [
  'rgba(255,0,0,0.2)',
  'rgba(255,100,0,0.2)',
  'rgba(255,200,0,0.2)',
  'rgba(100,255,0,0.2)',
  'rgba(0,255,100,0.2)',
  'rgba(0,100,255,0.2)',
  'rgba(0,0,255,0.2)',
  'rgba(100,0,255,0.2)',
];

export var ingredientBorderColours = [
  'rgba(255,0,0,0.4)',
  'rgba(255,100,0,0.4)',
  'rgba(255,200,0,0.4)',
  'rgba(100,255,0,0.4)',
  'rgba(0,255,100,0.4)',
  'rgba(0,100,255,0.4)',
  'rgba(0,0,255,0.4)',
  'rgba(100,0,255,0.4)',
];

export function calcTotalAttrs(selector) {
  var sugar = 0;
  var acid = 1.5;     // Produced during fermenation
  var tannin = 0;
  var solids = 0;
  var redness = 0;
  document.querySelectorAll(selector).forEach( ingr_row => {
    sugar += parseFloat(ingr_row.querySelector('.sugar').innerHTML);
    acid += parseFloat(ingr_row.querySelector('.acid').innerHTML);
    tannin += parseFloat(ingr_row.querySelector('.tannin').innerHTML);
    solids += parseFloat(ingr_row.querySelector('.solids').innerHTML);
    redness += parseFloat(ingr_row.querySelector('.redness').innerHTML);
  });
  return {
    sugar: sugar.toFixed(0),
    acid: acid.toFixed(2),
    tannin: tannin.toFixed(2),
    solids: solids.toFixed(2),
    redness: redness.toFixed(1),
  };
}

export function calcIngredientAttrs(ingredient, use, volume_l, profile) {
  var qty;

  // Convert qty to chosen units
  if ( profile ) {
    if (ingredient.liquid == 1000) {
      qty = liquid.convert(use.qty_kg, 0, profile.liquid_large_units);
    } else {
      qty = solid.convert(use.qty_kg, 0, profile.solid_large_units);
    }
  } else {
    qty = parseFloat(use.qty_kg);
  }

  return {
    id: ingredient.id,
    name: ingredient.name,
    variety: ingredient.variety,
    order: use.order,
    qty: qty.toFixed(3),
    sugar: (use.qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (use.qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (use.qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (use.qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (use.qty_kg * ingredient.redness / volume_l).toFixed(1),
  };
}

export var liquid;
export var solid;
var styles;
export function setUtilProfile(data) {
  liquid = new Converter(data.liquid);
  solid = new Converter(data.solid);
  styles = data.styles;
}

export function getStyleData(style_id) {
  var result =  {
    sugar: (0).toFixed(0),
    acid: (0).toFixed(2),
    tannin: (0).toFixed(2),
    solids: (0).toFixed(2),
  };
  styles.forEach( style => {
    if ( style.id == style_id ) {
      result = Object.assign({}, style);
      result.sugar = (result.alcohol * 7.5).toFixed(0);
      result.acid = result.acid.toFixed(2);
      result.tannin = result.tannin.toFixed(2);
      result.solids = result.solu_solid.toFixed(2);
    }
  });
  return result;
}

