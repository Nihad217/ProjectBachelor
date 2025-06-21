module com.example.projectbachelor {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.projectbachelor to javafx.fxml;
    exports com.example.projectbachelor;
}