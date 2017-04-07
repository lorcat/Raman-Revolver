function Ruby(id){
 var parent = id;
 var rb = this;
 
 var RB_BTN_PRESSURE = "#ruby_btn_p";
 var RB_REF = "#ruby_ref";
 var RB_VAL = "#ruby_value";
 var RB_MODEL = "#ruby_model";
 var RB_RESULT = "#ruby_result";
 
 var DEF_REF = 694.22;
 var DEF_VAL = 694.22;
 
 function initialize(){
  var content = " \
  <div id=\"ruby_header\" class=\"\">  \
  <h1> Ruby fluorescence pressure standard</h1> \
  </div>  \
  <div id=\"ruby_worker\" class=\"ruby_worker left\"> \
  <table class=\"table_worker\"> \
   <tr><td>Model: <td> <select id=\"ruby_model\" class=\"button\"> \
     <option name=\"Mao1978\" value=\"1\">M1978: non-hydrostatic [1]</option> \
     <option name=\"Mao1986\" value=\"2\">M1986: hydrostatic [2]</option> \
     <option name=\"Jacobsen2001\" value=\"3\">J2001: hydrostatic [3]</option> \
     <option name=\"Dewaele2008\" selected value=\"4\">D2008: hydrostatic [4]</option> \
    </select>\
   <tr><td>Reference line:<td><input type=\"text\" id=\"ruby_ref\" value=\"694.22\"> \
   <tr><td>Measured line:<td><input type=\"text\" id=\"ruby_value\" value=\"694.22\"> \
   <tr><td colspan=\"2\" class=\"right\"><span id=\"ruby_btn_p\" class=\"button button_static\" title=\"Calculate pressure as a function of Rb fluorescence signal\">Calculate Pressure</span> \
   <tr><td colspan=\"2\"><hr/> \
   <tr><td>Pressure:<td><div class=\"result\"><div><span id=\"ruby_result\">0</span>&nbsp; GPa</div></div>\
  </table> \
  </div> \
  <div id=\"ruby_footer\" class=\"left\"> \
  <table class=\"table_footer\"> \
  <tr><td>References:<td>\
  <tr><td><a href=\"http://dx.doi.org/10.1063/1.325277\" target=\"_blank\" >[1] Mao et al. 1978</a><td> - calibration 0.06 to 1 MBar \
  <tr><td><a href=\"http://dx.doi.org/10.1029/JB091iB05p04673\" target=\"_blank\">[2] Mao et al. 1986</a><td> - originally measured to 80 GPa<br/> \
  <tr><td><a href=\"http://dx.doi.org/10.2138/am.2008.2988\" target=\"_blank\">[3] Jacobsen et al. 2001</a><td> - correction for the range 23-140 GPa \
  <tr><td><a href=\"http://dx.doi.org/10.1103/PhysRevB.78.104102\" target=\"_blank\">[4] Dewaele et al. 2008</a><td> - one of the most recent to 200 GPa \
  </table></div>";
  
  $(content).appendTo(parent);
 }
 
 function initActions(){
  $(RB_BTN_PRESSURE).click(rb.calculate)
  .mouseover(function (){$(RB_BTN_PRESSURE).toggleClass("button_static button_over");})
  .mouseout(function (){$(RB_BTN_PRESSURE).toggleClass("button_static button_over");});

  $(RB_REF).keypress(function(e){
    if(e.which==13){
        rb.calculate()
    }
  });

  $(RB_VAL).keypress(function(e){
    if(e.which==13){
        rb.calculate()
    }
  });
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
  var obj = $(RB_RESULT);
  v = Math.round(v*100)/100;
  obj.html("<span class=\"ruby_result\">"+v+"</span>");
 }
 
 function calcRuby(v, r, A, B){
  //console.debug(v+" "r+" "A+" "B+" ");
  return A/B*(Math.pow(v/r,B)-1);
 }
 
 this.calculate = function(e){
  var ref, val, model;
  ref = getCheckDef(RB_REF, DEF_REF);
  val = getCheckDef(RB_VAL, DEF_VAL);
  model = parseInt(parseFloat($(RB_MODEL).val()));

  var A, B;
  A = 1904; B = 7.665;
  switch(model){
   case 1: //non hydrostatic
    B = 5;
    break;
   case 2:
    // Mao - hydrostatic
    break;
   case 3:
    // Jacobsen
    B = 10.32;
    break;
   case 4:
    // Dewaele
    A = 1920;
    B = 9.61;
    break;
  }
  reportValue(calcRuby(val, ref, A, B));
 }
 
 initialize();
 initActions();
};


function initialize_rb(parent){
    var parent = $(parent);

    var obj = $('<div id="ruby"><a name="ruby"></a><noscript> <div> This token (ruby) requires javascript for operation </div> </noscript></div>');
    $(parent).append(obj);

    var rb = new Ruby("#ruby");
}

