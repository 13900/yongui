import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.3
import "components"

Window {
    id: mainWindow
    width: 840
    height: 480
    visible: false
    title: qsTr("咏桂")

    property int offLoginWindow: 0
    property int pageSignal: 0

    Component.onCompleted: {

        // 创建并显示登录页面
        var loginComponent = Qt.createComponent("./components/LoginWindow.qml");
        var loginWindow = loginComponent.createObject(mainWindow);
        loginWindow.show();

        // 监听登录窗口的 closing 信号
        loginWindow.closing.connect(function() {
            // 更新状态变量
            if (offLoginWindow == 0){
//                user.email_quit()
                mainWindow.close()
                Qt.quit()
            }
        });

        user.onSuccessSignal.connect(function(x){

            offLoginWindow = x
            if (offLoginWindow === 1){
                loginWindow.close()
                mainWindow.visible = true
            }
        })

        user.onLogoutSignal.connect(function(){
            mainWindow.visible = false
            loginWindow.show()
        })
        pollingBar.onButtonClicked.connect(function(index){
                                               mainWindow.pageUpdate(index)
                                               mainWindow.pageSignal = index

                                           })

        sideBar.onButtonClick.connect(contentView.switchingPage)

    }

    function pageUpdate(index){
        pdf.set_grid_mode(index)
        contentView.reloadPage()
    }


    Flow {
        id: flow1
        anchors.fill: parent
    }



    PollingBar{
        id: pollingBar
        anchors.leftMargin: sideBar.width
    }

    ContentView {
        id: contentView
        width: parent.width - (sideBar.width + actionBar.width)
        height: parent.height
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottomMargin: 0
        anchors.topMargin: pollingBar.height
        anchors.leftMargin: sideBar.width
        anchors.rightMargin: actionBar.width

    }


    Sidebar {
        id: sideBar
        width: 60
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        color: "#d6d7d7"

    }

    ActionBar {
        id: actionBar
        width: 260
        height: parent.height
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.topMargin: pollingBar.height
        anchors.rightMargin: 0

    }

}
