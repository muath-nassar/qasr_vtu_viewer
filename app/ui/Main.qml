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

    // Top toolbar
    header: ToolBar {
        height: 40
        id: header
        background: Rectangle { color: darkBar }
        RowLayout {
            anchors.fill: parent
            spacing: 6
            Button { text: "Import VTU file"; onClicked: vm.show_dialog() }
            Button { text: "Import folder";   onClicked: vm.show_dialog() }
            Item   { Layout.fillWidth: true }
            Label  { text: vm.statusMessage; color: "#D0C8CB"; elide: Label.ElideRight; Layout.preferredWidth: 280 }
        }
    }

    // Bottom status bar
    footer: ToolBar {
        height: 30
        id: footer
        background: Rectangle { color: darkBar }
        RowLayout {
            anchors.fill: parent
            Label { text: "Status Bar"; color: "white"; Layout.leftMargin: 12 }
            Item  { Layout.fillWidth: true }
        }
    }

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
                    color: "#111"
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
                        text: modelData
                        highlighted: ListView.isCurrentItem
                        onClicked: ListView.view.currentIndex = index
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
