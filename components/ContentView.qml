import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.3
import QtWebEngine 1.9


Rectangle {


    id: root
    x: 0
    width: parent.width
    height: parent.height
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.bottomMargin: 0
    anchors.topMargin: 0
    clip: true



    Component.onCompleted: {
        pdfView.settings.pluginsEnabled = true;
        pdfView.settings.pluginApplication = true;
        pdfView.settings.shareOpenGLContexts = true;
        // 隐藏菜单按钮
        pdfView.setAttribute(WebEngineSettings.HideScrollbars, true)
        pdfView.setAttribute(WebEngineSettings.ShowMenuBar, false)
        pdfView.setAttribute(WebEngineSettings.ShowContextMenu, false)
        pdfView.setContextMenuPolicy(Qt.NoContextMenu)

    }


    function switchingPage(index){
        swipeView.currentIndex = index
    }

    function reloadPage(){
        pdfView.reload()
    }

    SwipeView {
        id: swipeView
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        interactive: false
        currentIndex: 0

        Rectangle {
            Column{
                width: parent.width
                height: parent.height
                WebEngineView {
                    id: pdfView
                    // 隐藏菜单按钮
                    anchors.fill: parent
                    url: "file:///resourceFiles/you_gui.pdf"

                }

            }
        }

        Rectangle {
            color: "green"
            Column{
                width: parent.width
                height: parent.height
                Text {
                    width: parent.width
                    id: name2
                    text: qsTr("text333")
                }

            }
        }

        Rectangle {
            color: "blue"
            Column{
                width: parent.width
                height: parent.height
                Text {
                    width: parent.width
                    id: name4
                    text: qsTr("text333")
                }

            }
        }

    }
}
