import QtQuick 2.9
import QtQuick.Window
import QtQuick.Controls 2.5
import QtQuick.Dialogs
import QtQuick.Controls.Material 2.3




Window {
    id: loginWindow
    width: 300
    height: 380
    color: "#2c2e2c"
    maximumWidth: 300
    minimumHeight: 380
    minimumWidth: 300
    visible: false
    title: "咏桂"
//    flags: Qt.Window | Qt.WindowStaysOnTopHint
    property int markNumber: 0

    Component.onCompleted:{
        loginPassword.editingFinished.connect(function(){

            if (loginName.text.trim().length !== 0) {
                if(loginName.text.includes("@qq.com") || loginName.text.includes("@163.com")){
                    user.login(loginName.text, loginPassword.text)
                }else{
                    message("邮箱格式不正确", "目前仅支持@qq.com邮箱和@163.com的邮箱")
                    loginNameRect.border.color = "red"
                }
            } else {
                 message("提示", "邮箱不能为空")
                loginNameRect.border.color = "red"
            }
        })

        verificationCode.editingFinished.connect(function(){


        })

        user.onFailureSignal.connect(function(){
            message("提示", "没有此用户")
            loginNameRect.border.color = "red"
            loginPasswordRect.border.color = "red"
        })

        user.onVerificationFinish.connect(function(x){
            if(x === 2){
                textCode.text = "注册"
                button1.background.color = "#999322"
                verificationCodeRect.border.color = "green"
                markNumber = 2
            }
        })
    }

    function message(title, text){
        var dialog = Qt.createQmlObject('import QtQuick.Dialogs; MessageDialog {}', loginWindow, "ErrorDialog");
        dialog.title = title;
        dialog.text = text;
        dialog.buttons = MessageDialog.Ok
        dialog.visible = true
    }

    Flow {
        id: flow1
        anchors.fill: parent

        Button {
            id: button
            x: 10
            y: 10
            width: 33
            height: 34
            text: qsTr("Button")
            icon.color: "#ffffff"
            icon.height: 50
            icon.width: 50
//            icon.source: "resourceFiles/images/chevrons-left.svg"
            icon.source: "../resourceFiles/images/chevrons-left.svg"
            property color defaultColor: "#2c2e2c"
            property int index: 0

            // 定义悬停状态的触发条件
            hoverEnabled: true
            background: Rectangle{
                color: button.defaultColor
            }
            onClicked: {
                if(button.index === 0){
                    button.index  = 1
                    loginName.text = ""
                    loginPassword.text = ""
                    swipeView.currentIndex = button.index
                }else{
                    button.index  = 0
                    registerName.text = ""
                    registerPassword.text = ""
                    swipeView.currentIndex = button.index
                }
            }
        }

        Image {
            id: image
            width: 100
            height: 100
            anchors.top: parent.top
            source: "../resourceFiles/images/calligraphy.png"
            anchors.topMargin: 60
            anchors.horizontalCenter: parent.horizontalCenter
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: text1
            width: 56
            height: 22
            color: "#fbf9f9"
            text: qsTr("咏桂")
            anchors.top: parent.top
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            anchors.topMargin: 180
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            id: rectangle
            width: 200
            height: 170
            color: "#2c2e2c"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.horizontalCenter: parent.horizontalCenter
            clip: true
            SwipeView {
                id: swipeView
                anchors.fill: parent
                interactive: false
                currentIndex: 0
                Item {
                    Text {
                        id: text3
                        x: 0
                        y: 20
                        width: 28
                        height: 23
                        color: "#9c9898"
                        text: qsTr("邮箱")
                        font.pixelSize: 12
                    }
                    Rectangle {
                        id: loginNameRect
                        x: 0
                        y: 49
                        width: 200
                        height: 30
                        color: "#242321"
                        radius: 13
                        border.color: "#e7de9c"
                        border.width: 2
                        TextInput {
                            id: loginName
                            width: 180
                            height: 30
                            color: "#fefefe"
                            text: qsTr("")
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 12
                            focus: true
                            clip: true
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                    Text {
                        id: text4
                        x: 0
                        y: 88
                        width: 28
                        height: 23
                        color: "#9c9898"
                        text: "密码"
                        font.pixelSize: 12
                    }
                    Rectangle {
                        id: loginPasswordRect
                        x: 0
                        y: 117
                        width: 200
                        height: 30
                        color: "#242321"
                        radius: 13
                        border.color: "#e7de9c"
                        border.width: 2
                        TextInput {
                            id: loginPassword
                            width: 180
                            height: 30
                            color: "#fefefe"
                            text: qsTr("")
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            echoMode: TextInput.Password
                            anchors.horizontalCenter: parent.horizontalCenter
                            clip: true
                            focus: true
                            }
                    }
                }
                Item {
                    id: item1
                    Text {
                        id: text5
                        x: 0
                        y: 74
                        width: 28
                        height: 23
                        color: "#9c9898"
                        text: "密码"
                        font.pixelSize: 12
                    }
                    Rectangle {
                        id: registerPasswordRect
                        x: 0
                        y: 97
                        width: 200
                        height: 30
                        color: "#242321"
                        radius: 13
                        border.color: "#e7de9c"
                        border.width: 2
                        TextInput {
                            id: registerPassword
                            width: 180
                            height: 30
                            color: "#fefefe"
                            text: qsTr("")
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                            clip: true
                            focus: true
                            echoMode: TextInput.Password
                        }
                    }
                    Text {
                        id: text6
                        x: 0
                        y: 8
                        width: 28
                        height: 23
                        color: "#9c9898"
                        text: qsTr("邮箱")
                        font.pixelSize: 12
                    }
                    Rectangle {
                        id: registerNameRect
                        x: 0
                        y: 32
                        width: 200
                        height: 30
                        color: "#242321"
                        radius: 13
                        border.color: "#e7de9c"
                        border.width: 2
                        TextInput {
                            id: registerName
                            width: 180
                            height: 30
                            color: "#fefefe"
                            text: qsTr("")
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                            clip: true
                            focus: true
                        }
                    }
                    Rectangle {
                        id: verificationCodeRect
                        x: 118
                        y: 65
                        width: 82
                        height: 24
                        color: "#242321"
                        radius: 13
                        border.color: "#e7de9c"
                        border.width: 2
                        TextInput {
                            id: verificationCode
                            width: 62
                            height: 24
                            color: "#fefefe"
                            PlaceholderText {
                                id: pal1
                                text: "验证码"
                                color: "#fefefe"
                                anchors.verticalCenter: parent.verticalCenter
                                font.pixelSize: 12
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                            clip: true
                            focus: true

                            onTextChanged: {
                                if(markNumber === 1){
                                    pal1.text = ""
                                    user.check_verification_code(verificationCode.text)
                                    verificationCodeRect.border.color = "red"
                                }
                            }
                        }
                    }

                    Button {
                        id: button1
                        y: 133
                        width: 90
                        height: 26
                        anchors.bottom: parent.bottom
                        font.pointSize: 12
                        icon.color: "#fffdfd"
                        anchors.bottomMargin: 8
                        anchors.horizontalCenter: parent.horizontalCenter
                        hoverEnabled: false
                        background: Rectangle{
                            color: "#2c4e36"
                            radius: 13
                        }
                        onClicked: {
                            if (registerName.text.trim().length !== 0 && registerPassword.text.trim().length !== 0) {
                                if(registerName.text.includes("@qq.com") || registerName.text.includes("@163.com")){
                                    registerNameRect.border.color = "green"
                                    registerPasswordRect.border.color = "green"
                                    if(markNumber === 0){
                                        user.send_verification_code(registerName.text)
                                        textCode.text = "验证码已发送"
                                        markNumber = 1
                                }
                                }else{
                                    message("邮箱格式不正确", "目前仅支持@qq.com邮箱和@163.com的邮箱")
                                    registerNameRect.border.color = "red"
                                }
                            } else {
                                 message("提示", "邮箱或密码不能为空")
                                registerPasswordRect.border.color = "red"
                                registerNameRect.border.color = "red"
                            }

                            if(markNumber === 2){
                                user.register(registerName.text, registerPassword.text)
                                registerName.text = ""
                                registerPassword.text = ""
                                verificationCode.text = ""
                                verificationCodeRect.border.color = "#e7de9c"
                                registerNameRect.border.color = "#e7de9c"
                                registerPasswordRect.border.color = "#e7de9c"
                                textCode.text = "发送验证码"
                                button1.background.color = "#2c4e36"
                                button.index  = 0
                                markNumber = 0
                                swipeView.currentIndex = button.index
                            }
                        }


                        Text {
                            id: textCode
                            text: "发送验证码"
                            anchors.fill: parent
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            font.family: "宋体"
                            font.pointSize: 10
                            font.bold: true
                            color: "#ffffff"
                        }
                    }
                }
            }
        }
    }

}


