import json


class CommandToScript:
    def __init__(self, deltaTimeScale):
        self.deltaTimeScale = deltaTimeScale

    def Process(self, commandFilePath, scriptFilePath):
        scriptText = ""
        with open(commandFilePath, 'r') as f:
            data = json.load(f)
            for command in data:
                scriptText += self.commandToString(command)
                scriptText += "\n"

        with open(scriptFilePath, 'w') as f:
            f.write(scriptText)

    def commandToString(self, commandElement):
        if commandElement == None:
            return ""
        outputText = self.commandTitleToString(commandElement)
        type = commandElement.get("Type")
        subTpye = commandElement.get("SubType")
        if type == "input":
            if subTpye == "keyboard":
                outputText += self.keyboardCommandToString(commandElement)
            elif subTpye == "mouse":
                outputText += self.mouseCommandToString(commandElement)
        elif type == "debug":
            outputText += self.debugCommandToString(commandElement)

        outputText += self.checkImage(commandElement)
        outputText += self.sleepToString(commandElement)
        return outputText

    def commandTitleToString(self, commandElement):
        if commandElement == None:
            return ""
        outputText = commandElement["Title"] + "\n"
        return outputText

    def mouseCommandToString(self, commandElement):
        if commandElement == None:
            return ""
        outputText = "\t{Key}Click {PosX} {PosY}\n".format(
            Key=commandElement["Key"], PosX=commandElement["PosX"], PosY=commandElement["PosY"])
        return outputText

    def keyboardCommandToString(self, commandElement):
        if commandElement == None:
            return ""
        outputText = "\tKeyInput {Key}\n".format(
            Key=commandElement["Key"])
        return outputText

    def debugCommandToString(self, commandElement):
        if commandElement == None:
            return ""
        outputText = "\tDebugCommand {Text}\n".format(
            Text=commandElement["Value"])
        return outputText

    def sleepToString(self, commandElement):
        if commandElement == None:
            return ""
        deltaTime = commandElement.get("DeltaTime")
        if deltaTime == None or deltaTime == 0:
            return ""
        millisecond = int(deltaTime * 1000 * self.deltaTimeScale)
        outputText = "\tSleep({DeltaTime})\n".format(
            DeltaTime=millisecond)
        return outputText

    def checkImage(self, commandElement):
        if commandElement == None:
            return ""
        checkElement = commandElement.get("Check")
        checkImage = commandElement.get("CheckImage")
        if checkElement == None or checkImage == None:
            return ""
        
        outputText = "\tImageCheck {FileName} {Score} {SX} {SY} {EX} {EY}\n".format(
            FileName=checkImage, Score=checkElement["Score"], SX=checkElement["Bound"][0], SY=checkElement["Bound"][1], EX=checkElement["Bound"][2], EY=checkElement["Bound"][3])
        return outputText
        





if __name__ == '__main__':
    CommandToScript = CommandToScript(1.0)
    CommandToScript.Process('./ScriptGenerator/CommandSample.json', './ScriptGenerator/Output.txt')
