<template>
    <div class="container-fluid bg-dark text-light p-3" data-bs-theme="dark">
        <!-- Nav tabs -->
        <ul class="nav nav-tabs" id="settingsTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="general-tab" data-bs-toggle="tab" data-bs-target="#general"
                    type="button" role="tab" aria-controls="general" aria-selected="true">
                    General Settings
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="graphics-tab" data-bs-toggle="tab" data-bs-target="#graphics" type="button"
                    role="tab" aria-controls="graphics" aria-selected="false">
                    Graphic Settings
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="hud-tab" data-bs-toggle="tab" data-bs-target="#hud" type="button"
                    role="tab" aria-controls="hud" aria-selected="false">
                    HUD Settings
                </button>
            </li>
        </ul>

        <!-- Tab panes -->
        <div class="tab-content mt-3">
            <!-- General Settings -->
            <div class="tab-pane fade show active" id="general" role="tabpanel" aria-labelledby="general-tab">
                <!-- CONTENIDO ORIGINAL -->
                <div class="input-group mb-3">
                    <!-- List of Game Publishers -->
                    <div class="form-floating">
                        <select class="form-select" id="cboGamePublisher" aria-label="Game Publisher:"
                            v-model="selectedPublisher" @change="OnGamePublisherChange">
                            <option v-for="(publisher, index) in publishers" :key="index" :value="index">
                                {{ publisher.instance }}
                            </option>
                        </select>
                        <label for="cboGamePublisher">Game Publisher:</label>
                    </div>
                    <!-- List of Game Versions -->
                    <div class="form-floating">
                        <select class="form-select" id="cboGameVersion" aria-label="Game Version:"
                            v-model="selectedVersion" @change="OnGameVersionChange">
                            <option v-for="(version, index) in versions" :key="index" :value="index">
                                {{ version.name }}
                            </option>
                        </select>
                        <label for="cboGameVersion">Game Version:</label>
                    </div>
                </div>

                <!-- Wine prefix / CrossOver bottle -->
                <div class="row">
                    <div class="col-12">
                        <label for="crossOverBottlePath">Wine Prefix / CrossOver Bottle Root:</label>
                        <div id="crossOverBottlePath" class="input-group mb-2">
                            <input type="text" class="form-control form-control-sm"
                                placeholder="Pick the CrossOver bottle folder that contains drive_c" aria-label="Pick a Location"
                                aria-describedby="button-addon-bottle" v-model="config.CrossOverBottlePath" />
                            <button class="btn btn-outline-secondary" type="button" id="button-addon-bottle"
                                @click="browseBottleFolder">
                                Browse
                            </button>
                        </div>
                        <div class="mb-3">
                            <button class="btn btn-outline-info btn-sm" type="button" @click="runCrossOverDllOverrides">
                                Repair Wine DLL Overrides
                            </button>
                            <span class="ms-2 text-muted small">{{ dllOverrideStatus }}</span>
                        </div>
                    </div>
                </div>

                <!-- Game Path Box -->
                <label for="txtFullGamePath" class="form-label">Full path to the Game's Executable:</label>
                <div class="input-group mb-3">
                    <input type="text" class="form-control form-control-sm"
                        placeholder="Manually select the game location or use the Localization Wizard below"
                        aria-label="Pick a location for " id="txtFullGamePath" v-model="selectedGamePath"
                        @change="OnGamePathChange" @input="OnGamePathChange" />
                    <button class="btn btn-outline-secondary" type="button" @click="browseGamePath()">
                        Browse
                    </button>
                </div>

                <!-- Additional paths and compatibility settings -->
                <div class="row">
                    <div class="col-12">
                        <label for="playerJournal">Player's Journal Location:</label>
                        <div id="playerJournal" class="input-group mb-3">
                            <input type="text" class="form-control form-control-sm"
                                placeholder="Pick a Location" aria-label="Pick a Location"
                                aria-describedby="button-addon2" v-model="config.PlayerJournal" />
                            <button class="btn btn-outline-secondary" type="button" id="button-addon2"
                                @click="browseJournalFolder">
                                Browse
                            </button>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12">
                        <label for="playerConfigFolder">Graphics Config XML Folder:</label>
                        <div id="playerConfigFolder" class="input-group mb-3">
                            <input type="text" class="form-control form-control-sm"
                                placeholder="Pick the folder containing GraphicsConfiguration*.xml" aria-label="Pick a Location"
                                aria-describedby="button-addon-config" v-model="config.PlayerConfigFolder" />
                            <button class="btn btn-outline-secondary" type="button" id="button-addon-config"
                                @click="browseConfigFolder">
                                Browse
                            </button>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-auto">
                        <label for="quantity">Number of Themes to Save:</label>
                        <input type="number" class="form-control form-control-sm" id="quantity" min="1" max="999" step="1"
                            inputmode="numeric" style="max-width: 5rem;" v-model="config.SavesToRemember" />
                    </div>
                </div>

                <!-- Footer buttons -->
                <div class="mt-4">
                    <div class="btn-group" role="group" aria-label="Default button group">
                        <button type="button" class="btn btn-outline-secondary" @click="CleanInstall">
                            Reset
                        </button>
                        <button type="button" class="btn btn-success" @click="runGameLocationAssistant">
                            Game Localization Wizard
                        </button>
                        <button type="button" class="btn btn-primary" @click="save">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>

            <!-- Graphic Settings -->
            <div class="tab-pane fade" id="graphics" role="tabpanel" aria-labelledby="graphics-tab">
                <div class="card text-light mb-3">
                    <div class="card-body">
                        <!-- Checkboxes -->
                        <div class="form-check" v-for="(label, key) in gpuCheckboxes" :key="key">
                            <input class="form-check-input" type="checkbox" :id="key" v-model="config[key]"
                                :disabled="!config.GpuAcceleration && (key === 'GpuSmoothScrolling')" />
                            <label class="form-check-label" :for="key">{{ label }}</label>
                        </div>

                        <!-- Renderer Select -->
                        <div class="mt-3">
                            <label for="gpuRenderer" class="form-label">GPU Renderer:</label>
                            <select id="gpuRenderer" class="form-select" v-model="config.GpuRenderer"
                                :disabled="!config.GpuAcceleration">
                                <option value="Vulkan">Vulkan</option>
                                <option value="OpenGL">OpenGL</option>
                                <option value="Direct3D">Direct3D</option>
                                <option value="dxmt">dxmt</option>
                            </select>
                        </div>

                        <!-- Font Size Select -->
                        <div class="mt-3">
                            <label for="fontSize" class="form-label">Font Size:</label>
                            <select id="fontSize" class="form-select" v-model="config.FontSize">
                                <option value="8px">8 px</option>
                                <option value="12px">12 px</option>
                                <option value="14px">14 px</option>
                                <option value="16px">16 px</option>
                                <option value="18px">18 px</option>
                                <option value="20px">20 px</option>
                                <option value="24px">24 px</option>
                                <option value="26px">26 px</option>
                                <option value="28px">28 px</option>
                            </select>
                        </div>

                         <!-- UI Scale Slider -->
                        <div class="mt-3">
                            <label for="uiScale" class="form-label">UI Scale (0 = Automatic):</label>
                            <input type="range" class="form-range" id="uiScale" min="0" max="3" step="0.25"
                                v-model.number="config.UiScaleFactor" @input="onUiScaleChange" />
                            <div class="small text-muted">
                                Value: {{ config.UiScaleFactor === 0 ? 'Automatic' : config.UiScaleFactor }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- HUD Settings -->
            <div class="tab-pane fade" id="hud" role="tabpanel" aria-labelledby="hud-tab">
                <div class="card text-light mb-3">
                    <div class="card-header">
                        <h5 class="mb-0">HUD Settings</h5>
                    </div>
                    <div class="card-body">
                        <p>Soon.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import EventBus from '../EventBus';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap';

export default {
    name: 'SettingsEditor',
    props: {
        initData: { type: Object, default: () => ({}) }
    },
    data() {
        return {
            visible: false,
            config: {},
            ActiveInstance: {},
            selectedPublisher: 0,
            selectedVersion: 0,
            selectedGamePath: '',
            dllOverrideStatus: 'Not checked',
            publishers: [],
            versions: [],
            DATA_DIRECTORY: '',
            gpuCheckboxes: {
                GpuSmoothScrolling: 'Smooth Scrolling',
                GpuAcceleration: 'Hardware Acceleration'
            }
        };
    },
    created() {
    },
    methods: {


        async Initialize() {
            try {
                if (this.config) {
                    console.log('Settings Loaded:', this.config);
                    // Ensure Default Values are set:
                    if (typeof this.config.CrossOverBottlePath === 'undefined') {
                        this.config.CrossOverBottlePath = '';
                    }
                    this.DATA_DIRECTORY = await window.api.resolveEnvVariables(this.config.UserDataFolder); //console.log('DATA_DIRECTORY:', DATA_DIRECTORY);

                    const instanceName = this.config.ActiveInstance; //<- "Steam (Odyssey (Live))"
                    const pubName = instanceName.split('(')[0];     //<- "Steam "
                    this.ActiveInstance = this.config.GameInstances
                        .flatMap(instance => instance.games)
                        .find(game => game.instance === instanceName);
                    console.log('ActiveInstance:', instanceName);

                    this.selectedGamePath = this.ActiveInstance.path;
                    if (!this.config.CrossOverBottlePath) {
                        this.config.CrossOverBottlePath = this.inferBottleRootFromPath(this.selectedGamePath);
                    }
                    this.selectedVersion = this.getGameVersionIndex(this.ActiveInstance.name);
                    this.selectedPublisher = this.getGameInstanceIndex(pubName);
                    this.publishers = this.config.GameInstances;
                    this.loadVersions();
                }
            } catch (error) {
                console.log(error);
            }
        },
        /* Button Click: Save the Settings */
        async save() {

            let selected = this.config.GameInstances[this.selectedPublisher].games[this.selectedVersion];
            //- Sets the path for the Active instance:
            if (selected.path != this.selectedGamePath) {
                selected.path = this.selectedGamePath;
            }

            //- Sets the Active Instance:
            this.config.ActiveInstance = selected.instance;

            window.api.events.sendEvent('SettingsChanged', JSON.parse(JSON.stringify(this.config))); //<- this event will be heard in 'App.vue'  
            window.api.settings.close();
        },

        loadVersions() {
            const selectedPublisherData = this.config.GameInstances[this.selectedPublisher];
            if (selectedPublisherData) {
                this.versions = selectedPublisherData.games;
                if (this.versions.length > 0) {
                    this.selectedVersion = 0;
                }
            } else {
                this.versions = [];
            }
        },

        OnGamePublisherChange(e) {
            const publisher = this.config.GameInstances[this.selectedPublisher];    //console.log(publisher);
            if (publisher) {
                this.ActiveInstance = publisher.games[0]; //console.log(this.ActiveInstance);
                this.config.ActiveInstance = this.ActiveInstance.instance;
                this.selectedGamePath = this.ActiveInstance.path;
                this.loadVersions();
            }
        },
        OnGameVersionChange(e) {
            const publisher = this.config.GameInstances[this.selectedPublisher];
            if (publisher) {
                this.ActiveInstance = publisher.games[this.selectedVersion];
                this.config.ActiveInstance = this.ActiveInstance.instance;
                this.selectedGamePath = this.ActiveInstance.path;
            }
        },
        async OnGamePathChange(e) {
            console.log('Selected Game Path:', this.selectedGamePath);
            // Check if EliteDangerous64.exe exists in the selected folder
            const filesInFolder = await window.api.readDirectory(this.selectedGamePath);
            const hasEliteExe = filesInFolder.includes('EliteDangerous64.exe');

            if (hasEliteExe) {
                console.log('[GamePath] Valid path selected:', this.selectedGamePath);
            } else {
                console.warn('[GamePath] EliteDangerous64.exe not found in selected folder:', this.selectedGamePath);
                window.api.events.sendEvent('RoastMe', {
                    type: 'Error',
                    message: 'EliteDangerous64.exe not found in the selected folder.<br>You can do it manually in the Game Instances...<br>or just click the Green Button.',
                    delay: 10000
                });
                return;
            }

            this.config.GameInstances[this.selectedPublisher].games[this.selectedVersion].path = this.selectedGamePath;
            this.config.ActiveInstance = this.config.GameInstances[this.selectedPublisher].games[this.selectedVersion].instance;

            console.log('ActiveInstance:', this.config.ActiveInstance);
        },

        onUiScaleChange() {
            // Broadcast al proceso principal o a otras ventanas
            window.api.settings.sendUiScale(this.config.UiScaleFactor);
        },

        getGameInstanceIndex(name) {
            switch (name.trim()) {
                case 'Steam': return 0;
                case 'Epic Games': return 1;
                case 'Frontier': return 2;
                default: return -1;
            }
        },
        getGameVersionIndex(name) {
            switch (name.trim()) {
                case 'Odyssey (Live)': return 0;
                case 'Horizons (Live)': return 1;
                case 'Horizons (Legacy)': return 2;
                default: return -1;
            }
        },
        inferPublisherIndexFromPath(gamePath) {
            const normalizedPath = (gamePath || '').toLowerCase();
            if (normalizedPath.includes('steamapps')) return this.getGameInstanceIndex('Steam');
            if (normalizedPath.includes('epic games') || normalizedPath.includes('epicgames')) return this.getGameInstanceIndex('Epic Games');
            if (normalizedPath.includes('frontier') || normalizedPath.includes('edlaunch')) return this.getGameInstanceIndex('Frontier');
            return -1;
        },
        inferBottleRootFromPath(hostPath) {
            if (!hostPath) return '';
            const normalizedPath = hostPath.replace(/\\/g, '/');
            const driveCMarker = '/drive_c/';
            const driveCIndex = normalizedPath.toLowerCase().indexOf(driveCMarker);
            if (driveCIndex < 0) return '';
            return normalizedPath.slice(0, driveCIndex);
        },
        async applyInferredBottlePaths(bottleRoot) {
            if (!bottleRoot) return;
            const inferredPaths = await window.api.getBottlePaths(bottleRoot);
            const isDefaultJournal = !this.config.PlayerJournal || this.config.PlayerJournal.includes('%USERPROFILE%');
            const isDefaultConfigFolder = !this.config.PlayerConfigFolder || this.config.PlayerConfigFolder.includes('%USERPROFILE%');
            if (!this.config.CrossOverBottlePath && inferredPaths.bottleRoot) {
                this.config.CrossOverBottlePath = inferredPaths.bottleRoot;
            }
            if (isDefaultJournal && inferredPaths.playerJournal) {
                this.config.PlayerJournal = inferredPaths.playerJournal;
            }
            if (isDefaultConfigFolder && inferredPaths.playerConfigFolder) {
                this.config.PlayerConfigFolder = inferredPaths.playerConfigFolder;
            }
        },

        /* Manually Browse for the Game Executable */
        async browseGamePath(params) {
            const platform = await window.api.getPlatform();
            const winDir = await window.api.resolveEnvVariables('%PROGRAMFILES%');
            const linuxDir = await window.api.resolveEnvVariables('%USERPROFILE%');
            const defaultLocation = this.selectedGamePath ? this.selectedGamePath :
                platform === 'win32' ? winDir : linuxDir;

            const options = {
                title: 'Select the Game Executable',
                defaultPath: defaultLocation,
                filters: [
                    { name: 'Game Executable', extensions: ['exe'] }
                ],
                properties: ['openFile', 'showHiddenFiles', 'dontAddToRecent'],
                message: 'Select the EliteDangerous64.exe location. On mac/CrossOver this is inside the bottle drive_c path.',
            };

            const filePath = await window.api.ShowOpenDialog(options);

            if (filePath && filePath.length > 0) {
                const selectedFile = filePath[0];
                const parentFolder = await window.api.getParentFolder(selectedFile);
                this.selectedGamePath = parentFolder;
                const inferredBottleRoot = this.inferBottleRootFromPath(selectedFile) || this.inferBottleRootFromPath(parentFolder);
                if (!this.config.CrossOverBottlePath) {
                    this.config.CrossOverBottlePath = inferredBottleRoot;
                }

                await this.applyInferredBottlePaths(this.config.CrossOverBottlePath || inferredBottleRoot);
                this.OnGamePathChange(null); // Trigger the change event to update the config
                if (!this.config.PlayerJournal) {
                    await this.browseJournalFolder();
                }
                if (!this.config.PlayerConfigFolder) {
                    await this.browseConfigFolder();
                }

            } else {
                console.log('[GamePath] No file selected.');
            }
        },
        /* Browse for the location where the ED Player Journal is located */
        async browseJournalFolder() {
            var defaultLocation = this.config.PlayerJournal ? this.config.PlayerJournal :
                '%USERPROFILE%\\Saved Games\\Frontier Developments\\Elite Dangerous';
            defaultLocation = await window.api.resolveEnvVariables(defaultLocation); //<- '%USERPROFILE%\\Saved Games\\Frontier Developments\\Elite Dangerous'
            console.log('defaultLocation:', defaultLocation);

            const options = {
                title: 'Select Where Game Stores Journal Files',
                defaultPath: defaultLocation,
                properties: ['openDirectory', 'createDirectory', 'promptToCreate', 'dontAddToRecent'],
                message: 'Select the folder containing Journal.*.log files',
                filters: null // No specific filters for directories
            };
            const filePath = await window.api.ShowOpenDialog(options);
            if (filePath) {
                this.config.PlayerJournal = filePath[0];
            }
        },
        async browseBottleFolder() {
            const defaultLocation = this.config.CrossOverBottlePath || await window.api.resolveEnvVariables('%USERPROFILE%');
            const options = {
                title: 'Select Wine Prefix / CrossOver Bottle Root',
                defaultPath: defaultLocation,
                properties: ['openDirectory', 'createDirectory', 'promptToCreate', 'dontAddToRecent'],
                message: 'Select the Wine prefix or CrossOver bottle folder that contains drive_c',
                filters: null
            };
            const filePath = await window.api.ShowOpenDialog(options);
            if (filePath) {
                this.config.CrossOverBottlePath = filePath[0];
            }
        },
        async runCrossOverDllOverrides() {
            try {
                if (!this.config.CrossOverBottlePath) {
                    await window.api.ShowMessageBox({
                        type: 'warning',
                        buttons: ['OK'],
                        title: 'Wine Prefix Required',
                        message: 'Select a CrossOver Bottle Root first.',
                        detail: 'The CrossOver bottle root is the folder that contains drive_c and user.reg.'
                    });
                    return;
                }

                const result = await window.api.setCrossOverDllOverrides(this.config.CrossOverBottlePath);
                this.dllOverrideStatus = result.skipped
                    ? 'Unavailable'
                    : (result.changed ? 'Repaired' : 'Configured');
                await window.api.ShowMessageBox({
                    type: result.changed ? 'info' : 'none',
                    buttons: ['OK'],
                    title: 'Wine DLL Overrides',
                    message: result.changed ? 'Wine DLL overrides were updated.' : 'Wine DLL overrides are already set.',
                    detail: result.changed
                        ? `Updated ${result.userRegPath}\nBackup: ${result.backupPath}\n\nRestart CrossOver/Elite if it was already running.`
                        : `Wine prefix / CrossOver bottle: ${result.bottleRoot}\n\nd3d11 and d3dcompiler_47 are set to native,builtin.`
                });
            } catch (error) {
                this.dllOverrideStatus = 'Error';
                console.log(error);
            }
        },
        async browseConfigFolder() {
            var defaultLocation = this.config.PlayerConfigFolder ? this.config.PlayerConfigFolder :
                '%USERPROFILE%\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\Graphics';
            defaultLocation = await window.api.resolveEnvVariables(defaultLocation);

            const options = {
                title: 'Select Graphics Config XML Folder',
                defaultPath: defaultLocation,
                properties: ['openDirectory', 'createDirectory', 'promptToCreate', 'dontAddToRecent'],
                message: 'Select the folder containing GraphicsConfiguration.xml and/or GraphicsConfigurationOverride.xml\nWindows default: %USERPROFILE%\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\Graphics',
                filters: null
            };
            const filePath = await window.api.ShowOpenDialog(options);
            if (filePath) {
                this.config.PlayerConfigFolder = filePath[0];
            }
        },

        /* Cleans html tags */
        sanitizeId(id) {
            return id.replace(/\s/g, '');
        },
        async InstallGameInstance(FolderPath) {
            return FolderPath;
        },

        /* Attempts to Detect the running Game Process and then sets the Paths */
        async runGameLocationAssistant() {
            const intro = await window.api.ShowMessageBox({
                type: 'info',
                buttons: ['Cancel', 'Continue'],
                defaultId: 1,
                cancelId: 0,
                title: 'Game Localization Wizard',
                message: 'This button detects the EliteDangerous64.exe location from a running Elite process.',
                detail: 'Before continuing, launch Elite Dangerous and leave it sitting at the main menu. The wizard will read the running game path and may need to close Elite before later file changes are applied.'
            });

            if (intro.response !== 1) {
                return;
            }

            const fullPath = await window.api.detectProgram('EliteDangerous64.exe');

            if (!fullPath) {
                await window.api.ShowMessageBox({
                    type: 'warning',
                    buttons: ['OK'],
                    defaultId: 0,
                    title: 'Elite Not Detected',
                    message: 'Elite Dangerous was not detected.',
                    detail: 'Launch Elite Dangerous, leave it at the main menu, then click the green button again.'
                });
                return;
            }

            console.log('Process found at:', fullPath);
            const translatedPath = await window.api.translateWindowsPath(fullPath);
            const hostExecutablePath = translatedPath && translatedPath !== fullPath ? translatedPath : fullPath;
            const FolderPath = await window.api.getParentFolder(hostExecutablePath);
            this.selectedGamePath = FolderPath; console.log('selectedGamePath', this.selectedGamePath);
            console.log('Selected Game Path:', this.selectedGamePath);
            const inferredBottleRoot = this.inferBottleRootFromPath(hostExecutablePath) || this.inferBottleRootFromPath(FolderPath) || this.inferBottleRootFromPath(fullPath);
            if (!this.config.CrossOverBottlePath) {
                this.config.CrossOverBottlePath = inferredBottleRoot;
            }
            await this.applyInferredBottlePaths(this.config.CrossOverBottlePath || inferredBottleRoot);
            if (this.config.CrossOverBottlePath) {
                const overrideResult = await window.api.ShowMessageBox({
                    type: 'question',
                    buttons: ['Not Now', 'Set EDHM DLL Overrides'],
                    defaultId: 1,
                    cancelId: 0,
                    title: 'CrossOver Bottle Detected',
                    message: 'Configure Wine DLL overrides for this prefix?',
                    detail: 'EDHM needs d3d11 and d3dcompiler_47 set to native,builtin. You can also run this later from the Wine Prefix / CrossOver Bottle Root row.'
                });
                if (overrideResult.response === 1) {
                    await this.runCrossOverDllOverrides();
                }
            }

            const inferredPublisherIndex = this.inferPublisherIndexFromPath(FolderPath);
            if (inferredPublisherIndex >= 0) {
                this.selectedPublisher = inferredPublisherIndex;
                this.loadVersions();
            }

            this.config.GameInstances[this.selectedPublisher].games[this.selectedVersion].path = this.selectedGamePath;
            this.config.ActiveInstance = this.config.GameInstances[this.selectedPublisher].games[this.selectedVersion].instance;
            console.log('ActiveInstance:', this.config.ActiveInstance);

            const closeResult = await window.api.ShowMessageBox({
                type: 'question',
                buttons: ['Leave Elite Running', 'Close Elite Now'],
                defaultId: 1,
                cancelId: 0,
                title: 'Game Path Detected',
                message: 'Elite was detected and the game folder was populated.',
                detail: `Detected folder:\n${FolderPath}\n\nClose Elite now if you want the app to continue with game-file changes more safely. Otherwise you can leave Elite running and close it yourself before applying changes.`
            });

            if (closeResult.response === 1) {
                await window.api.terminateProgram('EliteDangerous64.exe');
            }

            this.InstallGameInstance(this.selectedGamePath);
        },

        /** Button Click: Reset
         * Deletes the current settings file and the primary pointer file so the app starts fresh. */
        async CleanInstall() {
            try {
                const options = {
                    type: 'warning',
                    buttons: ['Cancel', 'Reset & Relaunch'],
                    defaultId: 1,
                    title: 'Reset Settings',
                    message: 'Reset EDHM-UI settings?',
                    detail: 'This deletes the current EDHM-UI settings and path selections, then restarts the app automatically.',
                    cancelId: 0,
                };
                const result = await window.api.ShowMessageBox(options); console.log(result);
                if (result.response === 1) {
                    const settingsFilePath = await window.api.resolveEnvVariables(await window.api.joinPath(this.config.UserDataFolder, 'Settings.json'));
                    const primarySettingsFilePath = await window.api.resolveEnvVariables('%EDHM_APPDATA%/Settings.json');
                    let deletedSomething = false;

                    if (await window.api.fileExists(settingsFilePath)) {
                        deletedSomething = await window.api.deleteFileByAbsolutePath(settingsFilePath) || deletedSomething;
                    }
                    if (await window.api.fileExists(primarySettingsFilePath)) {
                        deletedSomething = await window.api.deleteFileByAbsolutePath(primarySettingsFilePath) || deletedSomething;
                    }

                    this.config.PlayerJournal = '';
                    this.config.PlayerConfigFolder = '';
                    this.config.CrossOverBottlePath = '';
                    this.selectedGamePath = '';
                    await window.api.restartProgram();
                }
            } catch (error) {
                window.api.events.sendEvent('ShowError', error);
            }
        },

        async checkInstall(InstallStatus) {
            this.visible = true
            if (InstallStatus === 'existingInstall') {
                this.config = await window.api.getSettings()
                this.Initialize()
            } else {
                // FRESH INSTALL:
                this.config = await window.api.getDefaultSettings();
                if (typeof this.config.CrossOverBottlePath === 'undefined') {
                    this.config.CrossOverBottlePath = '';
                }
                this.Initialize();
            }
            
            if (typeof this.config.UiScaleFactor === 'undefined') {
                this.config.UiScaleFactor = 0;
            }
            console.log('uiScaleFactor:', this.config.UiScaleFactor)
        }
    },
    mounted() {
        window.api.settings.onInit((InstallStatus) => {
            console.log('initData@SettingsEditor.vue', InstallStatus);
            this.checkInstall(InstallStatus);
        })
    },
    beforeDestroy() {
        EventBus.off('open-settings-editor', this.open);
    }
}
</script>

<style scoped>
.modal-content {
    background-color: #343a40;
    color: #f8f9fa;
}

.accordion-button {
    background-color: #343a40;
    color: #f8f9fa;
}

.accordion-body {
    background-color: #343a40;
    color: #f8f9fa;
}

.form-control {
    background-color: #222;
    color: #f8f9fa;
    border-color: #666;
}
</style>
