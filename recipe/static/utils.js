class Converter {
  constructor(data) {
    this.units = data.units;    // array of tuples (id, string), where id is same as index
    this.conv = data.conv;      // array of conv factors indexed by id
    this.steps = data.step;      // array of spinner steps indexed by id
    this.decimals = data.decimals;   // array of decimal places to display indexed by id
  }

  convert(value) {
    return value * this.conv[this.currunit] / this.conv[0];
  }

  convert_back(value) {
    return value * this.conv[0] / this.conv[this.currunit];
  }

  set unit(unit) {
    this.currunit = unit;
  }

  get step() {
    return this.steps[this.currunit];
  }

  get decimal() {
    return this.decimals[this.currunit];
  }

  get string() {
    return this.units[this.currunit][1];
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
    if (ingr_row.querySelector('.redness')) {
      redness += parseFloat(ingr_row.querySelector('.redness').innerHTML);
    }
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
  var converter;
  var large_units;
  var small_units;

  if ( !profile ) {
    // User not logged in. Use default units.
    profile = {
      solid_small_units: 1,
      solid_large_units: 0,
      liquid_small_units: 1,
      liquid_large_units: 0,
    };
  }

  // Create a new converter with appropriate units and convert the quantity
  if (ingredient.is_solid) {
    converter = _.cloneDeep(solid);
    large_units = profile.solid_large_units;
    small_units = profile.solid_small_units;
  } else {
    converter = _.cloneDeep(liquid);
    large_units = profile.liquid_large_units;
    small_units = profile.liquid_small_units;
  }
  converter.unit = large_units;
  if (converter.convert(use.qty_kg) < 1 ) {
    converter.unit = small_units;
  }
  qty = converter.convert(use.qty_kg);
  ingredient.converter = converter;
  ingredient.large_units = large_units;
  ingredient.small_units = small_units;

  return {
    id: ingredient.id,
    name: ingredient.name,
    variety: ingredient.variety,
    order: use.order,
    qty: qty.toFixed(converter.decimal),
    qtystep: converter.step,
    unit: converter.string,
    sugar: (use.qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (use.qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (use.qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (use.qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (use.qty_kg * ingredient.redness / volume_l).toFixed(1),
  };
}

export function updateIngredientAttrs(ingredient, qty, order, volume_l) {
  var converter = ingredient.converter;
  var qty_kg;

  qty_kg = converter.convert_back(qty);

  converter.unit = ingredient.large_units;
  if (converter.convert(qty_kg) < 1 ) {
    converter.unit = ingredient.small_units;
  }
  qty = converter.convert(qty_kg);

  return {
    id: ingredient.id,
    name: ingredient.name,
    variety: ingredient.variety,
    order: order,
    qty: qty.toFixed(converter.decimal),
    qtystep: converter.step,
    qty_kg: qty_kg,
    unit: converter.string,
    sugar: (qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (qty_kg * ingredient.redness / volume_l).toFixed(1),
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

