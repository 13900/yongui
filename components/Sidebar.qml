import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.3
import QtQuick.Dialogs



Rectangle{
    id: root
    width: 60
    height: parent.height


    anchors.left: parent.left
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.margins: 0

    signal buttonClick(int index)

    Column {
        id: column
        width: 60
        height: parent.height - logOut.height
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        spacing: 0


        ListModel {
            id: buttonModel
            ListElement { text: "首页"; backgroundColor: "red"; icon: "../resourceFiles/images/home.svg" }
            ListElement { text: "导出"; backgroundColor: "red"; icon: "../resourceFiles/images/download-cloud.svg" }
            ListElement { text: "发送"; backgroundColor: "green"; icon: "../resourceFiles/images/send.svg" }
            ListElement { text: "关于"; backgroundColor: "green"; icon: "../resourceFiles/images/users.svg" }
            ListElement { text: "设置"; backgroundColor: "blue"; icon: "../resourceFiles/images/settings.svg" }
        }


        Rectangle {
            id: rectangle
            width: parent.width
            height: 200
            color: "#47f393"
        }
        FileDialog  {
                id: fileDialog
                title: "Save File"
                fileMode: FileDialog.SaveFile
                nameFilters: ["pdf Files (*.pdf)", "All Files (*)"]
                onAccepted: {
                    if (fileDialog.fileUrl !== ""){
                        var destination = fileDialog.currentFile
                        pdf.export_file(destination)
                    }

                }
            }

        Repeater {
            model: buttonModel
            Button {
                anchors.margins: 0
                width: parent.width
                height: 50
                icon.height: 15
                icon.width: 15
                ToolTip {
                    visible: hovered
                    Text{
                        text: model.text
                        color: "#838B83"
                    }
                    background: Rectangle{
                        color: "#F0FFF0"
                        radius: 5
                    }
                }
                icon.source: model.icon
//                background: Rectangle {
//                    color: model.backgroundColor
//                }

                onClicked: {
                    switch (index){
                        case 0:{
                            buttonClick(index)
                            break
                        }case 1:{
                            fileDialog.visible = true
                             break
                         }case 2:{
                              user.send_email_txt()
                              break
                          }case 3:{
                               buttonClick(index - 2)
                               break
                           }case 4:{
                                buttonClick(index - 2)
                                break
                            }
                    }



                }

            }
        }

    }

    Button{
        id: logOut
        width: parent.width
        height: 60
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        text: "注销"
        onClicked: {
            user.logout()
        }
    }
}
