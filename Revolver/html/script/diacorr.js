function DiamondCorrection(id){
 var parent = id;
 var dc = this;
 
 var DIACORR_BTN = "#diacorr_btn_p";

 var DIACORR_TIP = "#diacorr_tip";
 var DIACORR_BACK = "#diacorr_back";

 var DIACORR_RESULT = "#diacorr_result";
 
 var DEF_VAL = 0.000;

 var AIR_INDEX = 1.000293;
 var DIA_INDEX = 2.419;
 
 function initialize(){
  var content = " \
  <div id=\"diacorr_header\">  \
  <h1>Diamond correction</h1> \
  </div>  \
  <div id=\"diacorr_worker\" class=\"diacorr_worker\"> \
  <table class=\"table_worker\"> \
   <tr><td>X<sub>d. tip</sub><td><input type=\"text\" id=\"diacorr_tip\" value=\"0.000\"> \
   <tr><td>X<sub>d. back</sub><td><input type=\"text\" id=\"diacorr_back\" value=\"0.000\"> \
   <tr><td colspan=\"2\" class=\"right\"><span id=\"diacorr_btn_p\" class=\"button button_static\">Calculate Correction</span> \
   <tr><td colspan=\"2\" class=\"right\"><hr>\
   <tr><td>Sample position<td class=\"center\"><span id=\"diacorr_result\" class=\"result\"></span>\
  </table> \
  </div> \
  <div id=\"diacorr_footer\"> \
  </div>";
  
  $(content).appendTo(parent);
 }
 
 function initActions(){
  $(DIACORR_BTN).click(dc.calculate)
  .mouseover(function (){$(DIACORR_BTN).toggleClass("button_static button_over");})
  .mouseout(function (){$(DIACORR_BTN).toggleClass("button_static button_over");});


  var objs = [DIACORR_TIP, DIACORR_BACK];

  for(var i in objs){
    $(objs[i]).keypress(function(e){
        if(e.which==13){
            dc.calculate()
        }
    });
  }
 }

 function getCheckDef(sel, d){
  var res = $(sel).val();
  if(String(res).length==0){
   $(sel).val(new String(d));
   return d;
  }

  res = parseFloat(res);
  if(isNaN(res)){
    res = d;
  }
  return res;
 }
 
 function reportValue(v){
  $(DIACORR_RESULT).html(""+v.result.toFixed(4));
 }
 
 this.calculate = function(e){
  var tip, back, sample;
  try{

      tip = getCheckDef(DIACORR_TIP, DEF_VAL);
      back = getCheckDef(DIACORR_BACK, DEF_VAL);

      sample = back+Math.abs(back-tip)*DIA_INDEX/AIR_INDEX;
  }catch(err){
    console.debug(err);
    sample = NaN
  }

  var res = {"result": sample};
  reportValue(res);
 }
 
 initialize();
 initActions();
 dc.calculate();
};


function initialize_diacorr(parent, parent_button){
    var parent = $(parent);

    var obj = $('<div id="diacorr"><a name="diacorr"></a><noscript> <div> This token (diacorr) requires javascript for operation </div> </noscript></div>');
    $(parent).append(obj);

    var obj_button = $('<div class="tool_btn" id="diacorr_btn" title="Diamond correction calculation"><img src="images/dc.png"></div>');
    $(parent_button).append(obj_button);

    var dc = new DiamondCorrection("#diacorr");
}

