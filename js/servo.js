
Blockly.Blocks['initservo'] = {
  init: function() {
    this.setColour(235);
    this.appendDummyInput()
        .appendField("init servo")
        .appendField(new Blockly.FieldVariable('servo'), 'servo')
    this.setPreviousStatement(true);
    this.setInputsInline(true);
    this.setNextStatement(true);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('servo')];
  },
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('servo'))) {
      this.setFieldValue(newName, 'servo');
    }
  },
};
Blockly.Python['initservo'] = function(block) {
  var servo = block.getFieldValue('servo');
  var code = servo + " = servobot.servo()\n"
  return code;
};


Blockly.Blocks['servosetangle'] = {
  init: function() {
    this.setColour(235);
    this.appendDummyInput()
        .appendField("servo")
        .appendField(new Blockly.FieldVariable('servo'), 'servo')
        
    this.appendDummyInput()
        .appendField("angle")
        .appendField(new Blockly.FieldTextInput("40"), "angle")
        
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setInputsInline(true);
    this.setTooltip('');
  }
};
Blockly.Python['servosetangle'] = function(block) {
  var servo = block.getFieldValue('servo');
  var angle = block.getFieldValue('angle');
  var code = servo + ".set_angle("+ angle +")\n"
  return code;
};
