import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.3


//标题栏
    Row {
        id: root
        width: parent.width
        height: 40

        signal buttonClicked(int index)

        ListModel {
            id: buttonModel
            ListElement { text: "方格"; backgroundColor: "#ffffff"; index: 0 }
            ListElement { text: "田字格"; backgroundColor: "#ffffff"; index: 1 }
            ListElement { text: "米字格"; backgroundColor: "#ffffff"; index: 2 }
            ListElement { text: "交叉格"; backgroundColor: "#ffffff"; index: 3 }
            ListElement { text: "回宫格"; backgroundColor: "#ffffff"; index: 4 }
        }

        ListModel {
            id: buttonMode2
            ListElement { text: "行字帖"; backgroundColor: "#ffffff"; index: 5 }
            ListElement { text: "竖字帖"; backgroundColor: "#ffffff"; index: 6 }
            ListElement { text: "文章贴"; backgroundColor: "#ffffff"; index: 7 }
            ListElement { text: "拼音贴"; backgroundColor: "#ffffff"; index: 8 }
            ListElement { text: "经典诗词"; backgroundColor: "#ffffff"; index: 9 }
        }

        SwipeView {
            id: swipeView
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: rightButton.width
            anchors.topMargin: 0
            anchors.leftMargin: leftButton.width + 60

            currentIndex: 0
            // 添加需要切换的页面
            Rectangle {
                Row{
                    width: parent.width
                    height: parent.height
                Repeater {
                    model: buttonModel
                    Button {
                        width: (parent.width / 5)
                        height: parent.height
                        text: model.text
                        background: Rectangle {
                            color: model.backgroundColor
                        }

                        onClicked: {
                            root.buttonClicked(index)
                        }

                    }
                }
            }
        }

        Rectangle {
            Row{
                width: parent.width
                height: parent.height
            Repeater {
                model: buttonMode2
                Button {
                    width: (parent.width / 5)
                    height: parent.height
                    text: model.text
                    background: Rectangle {
                        color: model.backgroundColor
                    }

                    onClicked: {
                        root.buttonClicked(index)
                    }

                }
            }
        }
    }

//    Rectangle {
//        Row{
//            width: parent.width
//            height: parent.height
//        Repeater {
//            model: buttonModel
//            Button {
////                        width: parent.width
//                width: (parent.width / 5)
//                height: parent.height
//                text: model.text
//                background: Rectangle {
//                    color: model.backgroundColor
//                }

//                onClicked: {
//                    root.buttonClicked(index)

//                }

//            }
//        }
//    }
//}
}
        ToolButton {
            id: rightButton
            width: 40
            height: parent.height
            text: ">"
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.rightMargin: 0
            onClicked: swipeView.incrementCurrentIndex()
            background: Rectangle{
                color: "#ffffff"
            }
        }

        ToolButton {
            id: leftButton
            width: 40
            height: parent.height
            text: "<"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.leftMargin: 60
            background: Rectangle{
                color: "#ffffff"
            }
            onClicked: swipeView.decrementCurrentIndex()
        }

    }
