plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "sg.edwingarage.readonlybridge"
    compileSdk = 35

    defaultConfig {
        applicationId = "sg.edwingarage.readonlybridge"
        minSdk = 26
        targetSdk = 35
        versionCode = 3
        versionName = "2.0-manual-only"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    testImplementation("junit:junit:4.13.2")
}

// The existing assembleDebug workflow must pass the manual-only acceptance tests.
tasks.matching { it.name == "assembleDebug" }.configureEach {
    dependsOn("testDebugUnitTest")
}
