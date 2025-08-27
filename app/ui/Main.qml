import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 900
    height: 550
    title: "VTU Viewer — Non-recursive listing"
    header: ToolBar {
        RowLayout {
            spacing: 12
            Button {
                text: "Load VTU file"
                onClicked: vm.show_dialog()
            }
        }
    }
    ColumnLayout{
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        
        spacing: 16
        children: [

        ]

    }
}
