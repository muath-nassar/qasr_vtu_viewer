import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: win
    property color darkBar: "#4A3D3F"
    visible: true
    width: 1200
    height: 800
    color: "#E6DADA"
    title: "VTU Viewer"

    property string errorMessage: ""

    Dialog {
        id: errorDialog
        modal: false
        standardButtons: Dialog.Ok
        contentItem: Column {
            spacing: 8; padding: 16
            Label { text: errorMessage; wrapMode: Text.WordWrap }
        }

        // parent to the overlay then center against it
        parent: Overlay.overlay
        x: Math.round((parent.width  - width)  / 2)
        y: Math.round((parent.height - height) / 2)
    }


    // Listen to the VM signal (vm is the contextProperty you set in Python)
    Connections {
        target: vm
        function onErrorOccurred(message){
            errorMessage = message
            errorDialog.open()
            // Optional: console.log("VM error:", message)
        }
    }
    // Top toolbar
    header: ToolBar {
        height: 40
        id: header
        background: Rectangle { color: darkBar }
        RowLayout {
            anchors.fill: parent
            spacing: 6
            Button { text: "Import VTU file"; onClicked: vm.show_dialog() }
            Button { text: "fit all"; onClicked: vm.fitAll() }
            Item   { Layout.fillWidth: true }
            Button { text: "Import folder";   onClicked: vm.load_folder(folderPath.text) }
            TextField {
                Layout.preferredWidth: 300
                id: folderPath
                placeholderText: qsTr("Enter Folder Path")
            }

        }
    }

    // Bottom status bar
    footer: ToolBar {
        height: 30
        id: footer
        background: Rectangle { color: darkBar }
        RowLayout {
            anchors.fill: parent
            Label { 
                text: vm.state
                font.pixelSize: 14;
                color: "white"; Layout.leftMargin: 12 
                 }
            Item  { Layout.fillWidth: true }
        }
    }

    // Message Box for Errors


    // Main content: left list, center VTK view, right stack
    RowLayout {
        id: content
        anchors.fill: parent
        anchors.margins: 12
        spacing: 16

        // Left: Loaded Files
        Pane {
            id: leftPane
            Layout.preferredWidth: 200
            Layout.maximumWidth: 200
            Layout.fillHeight: true
            padding: 6
            background: Rectangle { color: darkBar; radius: 5 }

            ColumnLayout {
                anchors.fill: parent
                spacing: 8
                Label {
                    text: "Loaded Files"
                    color: "#ffffffff"
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: vm.files
                    clip: true
                    delegate: ItemDelegate {
                        width: ListView.view.width
                        contentItem: RowLayout {
                            spacing: 8
                            CheckBox {
                                id: vis
                                checked: true
                                onToggled: vm.toggleVisible(index, checked)
                            }
                            Label {
                                text: modelData
                                Layout.fillWidth: true
                                elide: Label.ElideRight
                            }
                        }
                    }
                }

            }
        }

        // Center: VTK View (placeholder)
        Pane {
            id: vtkPane
            Layout.fillWidth: true
            Layout.fillHeight: true
            padding: 12
            background: Rectangle { color: darkBar; radius: 5 }

            Rectangle {
                anchors.fill: parent
                radius: 5
                color: "transparent"
                border.color: "#6b6668"
                Text { anchors.centerIn: parent; text: "VTK View"; color: "#1a1a1a" }
            }
        }

        // Right: two stacked panels
        ColumnLayout {
            id: rightColumn
            Layout.preferredWidth: 150
            Layout.maximumWidth: 150
            Layout.fillHeight: true
            spacing: 16

            Pane {
                id: panel1
                Layout.fillWidth: true
                Layout.preferredHeight: (content.height - rightColumn.spacing) * 0.48
                padding: 12
                background: Rectangle { color: darkBar; radius: 5 }
                Label { text: "Panel1"; anchors.centerIn: parent; color: "#111" }
            }

            Pane {
                id: panel2
                Layout.preferredWidth: parent.width
                Layout.fillHeight: true
                padding: 12
                background: Rectangle { color: darkBar; radius: 5 }
                Label { text: "Panel2"; anchors.centerIn: parent; color: "#111" }
            }
        }
    }
}
