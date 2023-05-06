import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.3


ScrollView {
    id: scrollView
    x: 440
    width: 260
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.bottomMargin: 0
    anchors.topMargin: 0
    anchors.rightMargin: 0

    Column {
        id: column
        width: parent.width
        spacing: 10
        height: parent.height


        Text {
            id: text1
            text: qsTr("字帖内容：")
            font.pixelSize: 12
        }

        Rectangle{
            width: parent.width - 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            height: 150
            clip: true
            color: "#989477"


            Flickable {
                id: flickable
                width: parent.width
                height: parent.height
                contentWidth: parent.width
                contentHeight: textInput.contentHeight
                flickableDirection: Flickable.VerticalFlick

                TextEdit {
                    id: textInput
                    width: parent.width
                    height: parent.height
                    font.pixelSize: 12
                    wrapMode: TextInput.Wrap
                    selectByMouse: true
                    onTextChanged: {
                        pdf.set_text_content(textInput.text)
                        mainWindow.pageUpdate(mainWindow.pageSignal)
                    }

                }
            }
    }


        Text {
            id: text2
            text: qsTr("格子颜色：")
            font.pixelSize: 12

        }

        Row {
            id: row
            width: 260
            height: 50
            spacing: 5 // 设置子组件之间的间隔为10像素

            Button {
                id: button
                width: 45
                height: 40
                text: qsTr("绿色")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_line_color(143, 188, 143)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button1
                width: 45
                height: 40
                text: qsTr("蓝色")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_line_color(100,149,237)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button2
                width: 45
                height: 40
                text: qsTr("黑色")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_line_color(105,105,105)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button3
                width: 45
                height: 40
                text: qsTr("红色")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_line_color(178,34,34)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button4
                width: 45
                height: 40
                text: qsTr("紫色")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_line_color(186,85,211)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }
        }

        Row {
            id: row4
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text6
                height: 40
                text: qsTr("格子宽度：")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                id: button10
                width: 60
                height: 40
                text: qsTr("1.3cm")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_grid_size(1.3, 1.3)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button11
                width: 60
                height: 40
                text: qsTr("1.5cm")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_grid_size(1.5, 1.5)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button12
                width: 60
                height: 40
                text: qsTr("2cm")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_grid_size(2, 2)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }
        }

        Row {
            id: row1
            width: 200
            height: 50
            spacing: 5
            Text {
                id: text3
                text: qsTr("纸张大小：")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
            }

            Button {
                id: button5
                width: 40
                height: 40
                text: qsTr("A4")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_paper_mode(1)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button6
                width: 40
                height: 40
                text: qsTr("A3")
                anchors.verticalCenter: parent.verticalCenter
                font.letterSpacing: 0
                font.wordSpacing: 0
                onClicked: {
                    pdf.set_paper_mode(2)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }
        }

        Row {
            id: row2
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text4
                height: 40
                text: qsTr("描字类型：")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                id: button7
                width: 45
                height: 40
                text: qsTr("不描")
                anchors.verticalCenter: parent.verticalCenter

                onClicked: {
                    pdf.set_spelling(1)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button8
                width: 45
                height: 40
                text: qsTr("半描")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_spelling(2)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button9
                width: 45
                height: 40
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("全描")
                onClicked: {
                    pdf.set_spelling(3)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }

            }
        }

        Row {
            id: row23
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text43
                height: 40
                text: qsTr("描字透明度:")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                id: button73
                width: 45
                height: 40
                text: qsTr("0.2")
                anchors.verticalCenter: parent.verticalCenter

                onClicked: {
                    pdf.transparent_font(204,204,204)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button83
                width: 45
                height: 40
                text: qsTr("0.4")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.transparent_font(153, 153, 153)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button93
                width: 45
                height: 40
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("0.6")
                onClicked: {
                    pdf.transparent_font(119,119,119)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }

            }
        }

        Row {
            id: row3
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text5
                height: 40
                text: qsTr("字体风格：")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            ComboBox {
                id: comboBox
                height: 35
                anchors.verticalCenter: parent.verticalCenter
                model: ["方正楷体简体", "方正书宋简体", "衡山毛笔草书", "极字经典隶书", "三极小篆简", "英章行书"]
                onActivated: {
                    pdf.set_custom_fonts(currentIndex)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }
        }


        Row {
            id: row8
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text68
                height: 40
                text: qsTr("字体大小")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                id: button108
                width: 60
                height: 40
                text: qsTr("小")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_font_size(30)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button118
                width: 60
                height: 40
                text: qsTr("中")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_font_size(35)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button129
                width: 60
                height: 40
                text: qsTr("大")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_font_size(40)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }
        }

        Row {
            id: row83
            width: 200
            height: 50
            spacing: 5

            Text {
                id: text683
                height: 60
                text: qsTr("随机文本")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
            }

            Button {
                id: button1083
                width: 80
                height: 40
                text: qsTr("优美文章")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_text_content1(0)
                    pdf.set_spelling(3)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

            Button {
                id: button1183
                width: 80
                height: 40
                text: qsTr("经典诗词")
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    pdf.set_text_content1(1)
                    pdf.set_spelling(3)
                    mainWindow.pageUpdate(mainWindow.pageSignal)
                }
            }

        }

    }

}
