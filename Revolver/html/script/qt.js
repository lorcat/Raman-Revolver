/*
author: Konstantin Glazyrin
email: konstantin.glazyrin@desy.de

Should come after jsquery and plugins
Main proxy object/purpose for communications with qt application
*/

function ExternalCommunicationQt(){
    // main class taking care for external communications
    this.sel_macro_output = ".macro_output";
    this.sel_macro_info = ".macro_info";
    this.sel_macro_error = ".macro_error";
}

ExternalCommunicationQt.prototype.test = function(){
    // This is a simle test demonstrating communication of JS with Qt
    console.debug("ExtCom. : running test action");
    qtWindow.jsTest();
}

ExternalCommunicationQt.prototype.jsRunMacro = function(macro){
    // This is a simle test demonstrating communication of JS with Qt
    console.debug("ExtCom. : passing information on macro" + macro + " to qt");
    qtWindow.jsRunMacro(new String(macro));
}

ExternalCommunicationQt.prototype.processMacroResponse = function(output, info, error){
    // This is a simle test demonstrating communication of JS with Qt
    console.debug("ExtCom. : processing macro response");
    console.debug("ExtCom. : output - "+output);
    console.debug("ExtCom. : info - "+info);
    console.debug("ExtCom. : error - "+error);

    console.debug(info);

    // prepare string from an array

    output = this.arr2str(output);
    info = this.arr2str(info);
    error = this.arr2str(error);

    $(this.sel_macro_output).text(output);
    $(this.sel_macro_info).text(info);
    $(this.sel_macro_error).text(error);
}

ExternalCommunicationQt.prototype.arr2str = function(array){
    // This is a simle test demonstrating communication of JS with Qt
    console.debug("ExtCom. : converting array - "+array);

    var output = "";
    array.forEach(function(v, i){
        // strip service information
        v = v.replace(/\[[0-9]+m/g, "");
        output += v+"\n";
    });
    return output
}

// class for managing external communications with Qt
var ExtQt = new ExternalCommunicationQt();