/*
author: Konstantin Glazyrin
email: konstantin.glazyrin@desy.de

Object to control interaction with Qt and MacroServers
should be loaded after the jquery.js+qt.js
*/

function ExternalPositions(){
    // main class taking care for external communications
    this.sel_posname = ".posname"
}

ExternalPositions.prototype.get_name = function(){
    console.debug("Starting macro reading the name for position with sel. ("+this.sel_posname+")");
    var name = $(this.sel_posname).val();

    console.debug("Position name: "+name);
    return name
}

ExternalPositions.prototype.showpos = function(){
    console.debug("Starting macro showing the position");

    var name = this.get_name();
    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 showpos "+name
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.lspos = function(){
    console.debug("Starting macro showing the available positions");

    var name = this.get_name();

    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 lspos"
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.copyrb = function(){
    console.debug("Starting macro copying positions to the offline Raman and EH2 (GP) macro server");

    var name = this.get_name();

    console.debug("Saving the parameters to the offline ruby system")
    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 mempos_fixed "+name+" rbx %MOTX% rby %MOTY% rbz %MOTZ% rbzoom 100";
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.copygp = function(){
    console.debug("Starting macro copying positions to the offline Raman and EH2 (GP) macro server");

    var name = this.get_name();

    console.debug("Saving the parameters to the offline Raman system")
    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 mempos "+name+" ramanx ramany ramanz ramanfilt";
    ExtQt.jsRunMacro(mcro)

    mcro = "haspp02ch2.desy.de:10000/p02/door/haspp02ch2.02 mempos_fixed "+name+" cenx_gp %MOTX% ceny_gp %MOTY% samz_gp %MOTZ%";
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.copylh = function(){
    console.debug("Starting macro copying positions to the offline Raman and EH2 (LH) macro server");

    var name = this.get_name();

    console.debug("Saving the parameters to the offline Raman system")
    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 mempos "+name+" ramanx ramany ramanz ramanfilt";
    ExtQt.jsRunMacro(mcro)

    mcro = "haspp02ch2.desy.de:10000/p02/door/haspp02ch2.02 mempos_fixed "+name+" cenx_lh %MOTX% ceny_lh %MOTY% samz_lh %MOTZ%";
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.savepos = function(){
    console.debug("Starting macro copying positions to the offline Raman macro server");

    var name = this.get_name();

    console.debug("Saving the parameters to the offline Raman system")
    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 mempos "+name+" ramanx ramany ramanz ramanfilt";
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.cleanpos = function(){
    console.debug("Starting macro clearing the positions - deleting them");

    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 cleanpos .* 1 1";
    ExtQt.jsRunMacro(mcro)
}

ExternalPositions.prototype.moveto = function(){
    console.debug("Starting macro moving motors to the position");

    var name = $(this.sel_posname).val();

    mcro = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01 gopos "+name;
    ExtQt.jsRunMacro(mcro)
}

var ExtPos = new ExternalPositions()
