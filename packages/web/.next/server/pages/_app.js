"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/_app";
exports.ids = ["pages/_app"];
exports.modules = {

/***/ "__barrel_optimize__?names=Box,IconButton!=!./node_modules/@mui/material/index.js":
/*!****************************************************************************************!*\
  !*** __barrel_optimize__?names=Box,IconButton!=!./node_modules/@mui/material/index.js ***!
  \****************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {\n__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   Box: () => (/* reexport safe */ _Box_index_js__WEBPACK_IMPORTED_MODULE_0__[\"default\"]),\n/* harmony export */   IconButton: () => (/* reexport safe */ _IconButton_index_js__WEBPACK_IMPORTED_MODULE_1__[\"default\"])\n/* harmony export */ });\n/* harmony import */ var _Box_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Box/index.js */ \"./node_modules/@mui/material/Box/index.js\");\n/* harmony import */ var _IconButton_index_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./IconButton/index.js */ \"./node_modules/@mui/material/IconButton/index.js\");\nvar __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([_IconButton_index_js__WEBPACK_IMPORTED_MODULE_1__]);\n_IconButton_index_js__WEBPACK_IMPORTED_MODULE_1__ = (__webpack_async_dependencies__.then ? (await __webpack_async_dependencies__)() : __webpack_async_dependencies__)[0];\n\n\n\n__webpack_async_result__();\n} catch(e) { __webpack_async_result__(e); } });//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiX19iYXJyZWxfb3B0aW1pemVfXz9uYW1lcz1Cb3gsSWNvbkJ1dHRvbiE9IS4vbm9kZV9tb2R1bGVzL0BtdWkvbWF0ZXJpYWwvaW5kZXguanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFDK0MiLCJzb3VyY2VzIjpbIi9Vc2Vycy9kYXZpZC9EZXNrdG9wL2RldmVsb3BtZW50L2F1ZGFmYWN0L3BhY2thZ2VzL3dlYi9ub2RlX21vZHVsZXMvQG11aS9tYXRlcmlhbC9pbmRleC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJcbmV4cG9ydCB7IGRlZmF1bHQgYXMgQm94IH0gZnJvbSBcIi4vQm94L2luZGV4LmpzXCJcbmV4cG9ydCB7IGRlZmF1bHQgYXMgSWNvbkJ1dHRvbiB9IGZyb20gXCIuL0ljb25CdXR0b24vaW5kZXguanNcIiJdLCJuYW1lcyI6W10sImlnbm9yZUxpc3QiOlswXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///__barrel_optimize__?names=Box,IconButton!=!./node_modules/@mui/material/index.js\n");

/***/ }),

/***/ "./src/context/AnalysisContext.tsx":
/*!*****************************************!*\
  !*** ./src/context/AnalysisContext.tsx ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   AnalysisProvider: () => (/* binding */ AnalysisProvider),\n/* harmony export */   useAnalysis: () => (/* binding */ useAnalysis)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n\n\nconst analysisReducer = (state, action)=>{\n    switch(action.type){\n        case 'START_ANALYSIS':\n            return {\n                ...state,\n                loading: true,\n                error: null\n            };\n        case 'ANALYSIS_SUCCESS':\n            return {\n                results: action.payload,\n                loading: false,\n                error: null\n            };\n        case 'ANALYSIS_ERROR':\n            return {\n                ...state,\n                loading: false,\n                error: action.payload\n            };\n        case 'RESET_ANALYSIS':\n            return {\n                results: null,\n                loading: false,\n                error: null\n            };\n        default:\n            return state;\n    }\n};\nconst AnalysisContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)(undefined);\nconst initialState = {\n    results: null,\n    loading: false,\n    error: null\n};\nconst AnalysisProvider = ({ children })=>{\n    const [state, dispatch] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useReducer)(analysisReducer, initialState);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(AnalysisContext.Provider, {\n        value: {\n            state,\n            dispatch\n        },\n        children: children\n    }, void 0, false, {\n        fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/context/AnalysisContext.tsx\",\n        lineNumber: 66,\n        columnNumber: 5\n    }, undefined);\n};\nconst useAnalysis = ()=>{\n    const context = (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(AnalysisContext);\n    if (!context) {\n        throw new Error('useAnalysis must be used within an AnalysisProvider');\n    }\n    return context;\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvY29udGV4dC9BbmFseXNpc0NvbnRleHQudHN4IiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBcUU7QUFlckUsTUFBTUksa0JBQWtCLENBQUNDLE9BQXNCQztJQUM3QyxPQUFRQSxPQUFPQyxJQUFJO1FBQ2pCLEtBQUs7WUFDSCxPQUFPO2dCQUNMLEdBQUdGLEtBQUs7Z0JBQ1JHLFNBQVM7Z0JBQ1RDLE9BQU87WUFDVDtRQUVGLEtBQUs7WUFDSCxPQUFPO2dCQUNMQyxTQUFTSixPQUFPSyxPQUFPO2dCQUN2QkgsU0FBUztnQkFDVEMsT0FBTztZQUNUO1FBRUYsS0FBSztZQUNILE9BQU87Z0JBQ0wsR0FBR0osS0FBSztnQkFDUkcsU0FBUztnQkFDVEMsT0FBT0gsT0FBT0ssT0FBTztZQUN2QjtRQUVGLEtBQUs7WUFDSCxPQUFPO2dCQUNMRCxTQUFTO2dCQUNURixTQUFTO2dCQUNUQyxPQUFPO1lBQ1Q7UUFFRjtZQUNFLE9BQU9KO0lBQ1g7QUFDRjtBQUVBLE1BQU1PLGdDQUFrQlgsb0RBQWFBLENBR3RCWTtBQUVmLE1BQU1DLGVBQThCO0lBQ2xDSixTQUFTO0lBQ1RGLFNBQVM7SUFDVEMsT0FBTztBQUNUO0FBRU8sTUFBTU0sbUJBQTRELENBQUMsRUFBRUMsUUFBUSxFQUFFO0lBQ3BGLE1BQU0sQ0FBQ1gsT0FBT1ksU0FBUyxHQUFHZCxpREFBVUEsQ0FBQ0MsaUJBQWlCVTtJQUV0RCxxQkFDRSw4REFBQ0YsZ0JBQWdCTSxRQUFRO1FBQUNDLE9BQU87WUFBRWQ7WUFBT1k7UUFBUztrQkFDaEREOzs7Ozs7QUFHUCxFQUFFO0FBRUssTUFBTUksY0FBYztJQUN6QixNQUFNQyxVQUFVbkIsaURBQVVBLENBQUNVO0lBQzNCLElBQUksQ0FBQ1MsU0FBUztRQUNaLE1BQU0sSUFBSUMsTUFBTTtJQUNsQjtJQUNBLE9BQU9EO0FBQ1QsRUFBRSIsInNvdXJjZXMiOlsiL1VzZXJzL2RhdmlkL0Rlc2t0b3AvZGV2ZWxvcG1lbnQvYXVkYWZhY3QvcGFja2FnZXMvd2ViL3NyYy9jb250ZXh0L0FuYWx5c2lzQ29udGV4dC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0LCB7IGNyZWF0ZUNvbnRleHQsIHVzZUNvbnRleHQsIHVzZVJlZHVjZXIgfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgdHlwZSB7IEFuYWx5c2lzUmVzcG9uc2UgfSBmcm9tICcuLi90eXBlcy9hcGknO1xuXG5pbnRlcmZhY2UgQW5hbHlzaXNTdGF0ZSB7XG4gIHJlc3VsdHM6IEFuYWx5c2lzUmVzcG9uc2UgfCBudWxsO1xuICBsb2FkaW5nOiBib29sZWFuO1xuICBlcnJvcjogRXJyb3IgfCBudWxsO1xufVxuXG50eXBlIEFuYWx5c2lzQWN0aW9uID0gXG4gIHwgeyB0eXBlOiAnU1RBUlRfQU5BTFlTSVMnIH1cbiAgfCB7IHR5cGU6ICdBTkFMWVNJU19TVUNDRVNTJzsgcGF5bG9hZDogQW5hbHlzaXNSZXNwb25zZSB9XG4gIHwgeyB0eXBlOiAnQU5BTFlTSVNfRVJST1InOyBwYXlsb2FkOiBFcnJvciB9XG4gIHwgeyB0eXBlOiAnUkVTRVRfQU5BTFlTSVMnIH07XG5cbmNvbnN0IGFuYWx5c2lzUmVkdWNlciA9IChzdGF0ZTogQW5hbHlzaXNTdGF0ZSwgYWN0aW9uOiBBbmFseXNpc0FjdGlvbik6IEFuYWx5c2lzU3RhdGUgPT4ge1xuICBzd2l0Y2ggKGFjdGlvbi50eXBlKSB7XG4gICAgY2FzZSAnU1RBUlRfQU5BTFlTSVMnOlxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgLi4uc3RhdGUsXG4gICAgICAgIGxvYWRpbmc6IHRydWUsXG4gICAgICAgIGVycm9yOiBudWxsXG4gICAgICB9O1xuICAgIFxuICAgIGNhc2UgJ0FOQUxZU0lTX1NVQ0NFU1MnOlxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgcmVzdWx0czogYWN0aW9uLnBheWxvYWQsXG4gICAgICAgIGxvYWRpbmc6IGZhbHNlLFxuICAgICAgICBlcnJvcjogbnVsbFxuICAgICAgfTtcbiAgICBcbiAgICBjYXNlICdBTkFMWVNJU19FUlJPUic6XG4gICAgICByZXR1cm4ge1xuICAgICAgICAuLi5zdGF0ZSxcbiAgICAgICAgbG9hZGluZzogZmFsc2UsXG4gICAgICAgIGVycm9yOiBhY3Rpb24ucGF5bG9hZFxuICAgICAgfTtcbiAgICBcbiAgICBjYXNlICdSRVNFVF9BTkFMWVNJUyc6XG4gICAgICByZXR1cm4ge1xuICAgICAgICByZXN1bHRzOiBudWxsLFxuICAgICAgICBsb2FkaW5nOiBmYWxzZSxcbiAgICAgICAgZXJyb3I6IG51bGxcbiAgICAgIH07XG4gICAgXG4gICAgZGVmYXVsdDpcbiAgICAgIHJldHVybiBzdGF0ZTtcbiAgfVxufTtcblxuY29uc3QgQW5hbHlzaXNDb250ZXh0ID0gY3JlYXRlQ29udGV4dDx7XG4gIHN0YXRlOiBBbmFseXNpc1N0YXRlO1xuICBkaXNwYXRjaDogUmVhY3QuRGlzcGF0Y2g8QW5hbHlzaXNBY3Rpb24+O1xufSB8IHVuZGVmaW5lZD4odW5kZWZpbmVkKTtcblxuY29uc3QgaW5pdGlhbFN0YXRlOiBBbmFseXNpc1N0YXRlID0ge1xuICByZXN1bHRzOiBudWxsLFxuICBsb2FkaW5nOiBmYWxzZSxcbiAgZXJyb3I6IG51bGxcbn07XG5cbmV4cG9ydCBjb25zdCBBbmFseXNpc1Byb3ZpZGVyOiBSZWFjdC5GQzx7IGNoaWxkcmVuOiBSZWFjdC5SZWFjdE5vZGUgfT4gPSAoeyBjaGlsZHJlbiB9KSA9PiB7XG4gIGNvbnN0IFtzdGF0ZSwgZGlzcGF0Y2hdID0gdXNlUmVkdWNlcihhbmFseXNpc1JlZHVjZXIsIGluaXRpYWxTdGF0ZSk7XG5cbiAgcmV0dXJuIChcbiAgICA8QW5hbHlzaXNDb250ZXh0LlByb3ZpZGVyIHZhbHVlPXt7IHN0YXRlLCBkaXNwYXRjaCB9fT5cbiAgICAgIHtjaGlsZHJlbn1cbiAgICA8L0FuYWx5c2lzQ29udGV4dC5Qcm92aWRlcj5cbiAgKTtcbn07XG5cbmV4cG9ydCBjb25zdCB1c2VBbmFseXNpcyA9ICgpID0+IHtcbiAgY29uc3QgY29udGV4dCA9IHVzZUNvbnRleHQoQW5hbHlzaXNDb250ZXh0KTtcbiAgaWYgKCFjb250ZXh0KSB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCd1c2VBbmFseXNpcyBtdXN0IGJlIHVzZWQgd2l0aGluIGFuIEFuYWx5c2lzUHJvdmlkZXInKTtcbiAgfVxuICByZXR1cm4gY29udGV4dDtcbn07XG4iXSwibmFtZXMiOlsiUmVhY3QiLCJjcmVhdGVDb250ZXh0IiwidXNlQ29udGV4dCIsInVzZVJlZHVjZXIiLCJhbmFseXNpc1JlZHVjZXIiLCJzdGF0ZSIsImFjdGlvbiIsInR5cGUiLCJsb2FkaW5nIiwiZXJyb3IiLCJyZXN1bHRzIiwicGF5bG9hZCIsIkFuYWx5c2lzQ29udGV4dCIsInVuZGVmaW5lZCIsImluaXRpYWxTdGF0ZSIsIkFuYWx5c2lzUHJvdmlkZXIiLCJjaGlsZHJlbiIsImRpc3BhdGNoIiwiUHJvdmlkZXIiLCJ2YWx1ZSIsInVzZUFuYWx5c2lzIiwiY29udGV4dCIsIkVycm9yIl0sImlnbm9yZUxpc3QiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./src/context/AnalysisContext.tsx\n");

/***/ }),

/***/ "./src/pages/_app.tsx":
/*!****************************!*\
  !*** ./src/pages/_app.tsx ***!
  \****************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {\n__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   ColorModeContext: () => (/* binding */ ColorModeContext),\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/styles */ \"./node_modules/@mui/material/node/styles/index.js\");\n/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_mui_material_styles__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _mui_material_CssBaseline__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/CssBaseline */ \"./node_modules/@mui/material/node/CssBaseline/index.js\");\n/* harmony import */ var _theme__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../theme */ \"./src/theme/index.ts\");\n/* harmony import */ var _barrel_optimize_names_Box_IconButton_mui_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! __barrel_optimize__?names=Box,IconButton!=!@mui/material */ \"__barrel_optimize__?names=Box,IconButton!=!./node_modules/@mui/material/index.js\");\n/* harmony import */ var _mui_icons_material_Brightness4__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/icons-material/Brightness4 */ \"./node_modules/@mui/icons-material/esm/Brightness4.js\");\n/* harmony import */ var _mui_icons_material_Brightness7__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/icons-material/Brightness7 */ \"./node_modules/@mui/icons-material/esm/Brightness7.js\");\n/* harmony import */ var _context_AnalysisContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../context/AnalysisContext */ \"./src/context/AnalysisContext.tsx\");\nvar __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([_barrel_optimize_names_Box_IconButton_mui_material__WEBPACK_IMPORTED_MODULE_6__]);\n_barrel_optimize_names_Box_IconButton_mui_material__WEBPACK_IMPORTED_MODULE_6__ = (__webpack_async_dependencies__.then ? (await __webpack_async_dependencies__)() : __webpack_async_dependencies__)[0];\n\n\n\n\n\n\n\n\n// Create a context for theme mode\n\nconst ColorModeContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)({\n    toggleColorMode: ()=>{}\n});\n\nfunction MyApp({ Component, pageProps }) {\n    const [mode, setMode] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('dark');\n    const colorMode = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)({\n        \"MyApp.useMemo[colorMode]\": ()=>({\n                toggleColorMode: ({\n                    \"MyApp.useMemo[colorMode]\": ()=>{\n                        setMode({\n                            \"MyApp.useMemo[colorMode]\": (prevMode)=>prevMode === 'light' ? 'dark' : 'light'\n                        }[\"MyApp.useMemo[colorMode]\"]);\n                    }\n                })[\"MyApp.useMemo[colorMode]\"]\n            })\n    }[\"MyApp.useMemo[colorMode]\"], []);\n    const theme = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)({\n        \"MyApp.useMemo[theme]\": ()=>(0,_theme__WEBPACK_IMPORTED_MODULE_2__.createAppTheme)(mode)\n    }[\"MyApp.useMemo[theme]\"], [\n        mode\n    ]);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_context_AnalysisContext__WEBPACK_IMPORTED_MODULE_3__.AnalysisProvider, {\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(ColorModeContext.Provider, {\n            value: colorMode,\n            children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_mui_material_styles__WEBPACK_IMPORTED_MODULE_4__.ThemeProvider, {\n                theme: theme,\n                children: [\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_mui_material_CssBaseline__WEBPACK_IMPORTED_MODULE_5__[\"default\"], {}, void 0, false, {\n                        fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                        lineNumber: 35,\n                        columnNumber: 11\n                    }, this),\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_IconButton_mui_material__WEBPACK_IMPORTED_MODULE_6__.Box, {\n                        sx: {\n                            position: 'fixed',\n                            top: 16,\n                            right: 16,\n                            zIndex: 1000\n                        },\n                        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_IconButton_mui_material__WEBPACK_IMPORTED_MODULE_6__.IconButton, {\n                            onClick: colorMode.toggleColorMode,\n                            color: \"inherit\",\n                            sx: {\n                                bgcolor: 'background.paper',\n                                '&:hover': {\n                                    bgcolor: 'background.paper',\n                                    opacity: 0.9\n                                }\n                            },\n                            children: mode === 'dark' ? /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_mui_icons_material_Brightness7__WEBPACK_IMPORTED_MODULE_7__[\"default\"], {}, void 0, false, {\n                                fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                                lineNumber: 55,\n                                columnNumber: 34\n                            }, this) : /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_mui_icons_material_Brightness4__WEBPACK_IMPORTED_MODULE_8__[\"default\"], {}, void 0, false, {\n                                fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                                lineNumber: 55,\n                                columnNumber: 56\n                            }, this)\n                        }, void 0, false, {\n                            fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                            lineNumber: 44,\n                            columnNumber: 13\n                        }, this)\n                    }, void 0, false, {\n                        fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                        lineNumber: 36,\n                        columnNumber: 11\n                    }, this),\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(Component, {\n                        ...pageProps\n                    }, void 0, false, {\n                        fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                        lineNumber: 58,\n                        columnNumber: 11\n                    }, this)\n                ]\n            }, void 0, true, {\n                fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n                lineNumber: 34,\n                columnNumber: 9\n            }, this)\n        }, void 0, false, {\n            fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n            lineNumber: 33,\n            columnNumber: 7\n        }, this)\n    }, void 0, false, {\n        fileName: \"/Users/david/Desktop/development/audafact/packages/web/src/pages/_app.tsx\",\n        lineNumber: 32,\n        columnNumber: 5\n    }, this);\n}\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MyApp);\n\n__webpack_async_result__();\n} catch(e) { __webpack_async_result__(e); } });//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvcGFnZXMvX2FwcC50c3giLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQTBDO0FBQ1c7QUFDRDtBQUNWO0FBQ007QUFDYztBQUNBO0FBRTlELGtDQUFrQztBQUNJO0FBQy9CLE1BQU1VLGlDQUFtQkQsb0RBQWFBLENBQUM7SUFDNUNFLGlCQUFpQixLQUFPO0FBQzFCLEdBQUc7QUFFMkQ7QUFFOUQsU0FBU0UsTUFBTSxFQUFFQyxTQUFTLEVBQUVDLFNBQVMsRUFBRTtJQUNyQyxNQUFNLENBQUNDLE1BQU1DLFFBQVEsR0FBR2pCLCtDQUFRQSxDQUFtQjtJQUVuRCxNQUFNa0IsWUFBWWpCLDhDQUFPQTtvQ0FDdkIsSUFBTztnQkFDTFUsZUFBZTtnREFBRTt3QkFDZk07d0RBQVEsQ0FBQ0UsV0FBY0EsYUFBYSxVQUFVLFNBQVM7O29CQUN6RDs7WUFDRjttQ0FDQSxFQUFFO0lBR0osTUFBTUMsUUFBUW5CLDhDQUFPQTtnQ0FBQyxJQUFNRyxzREFBY0EsQ0FBQ1k7K0JBQU87UUFBQ0E7S0FBSztJQUV4RCxxQkFDRSw4REFBQ0osc0VBQWdCQTtrQkFDZiw0RUFBQ0YsaUJBQWlCVyxRQUFRO1lBQUNDLE9BQU9KO3NCQUNoQyw0RUFBQ2hCLCtEQUFhQTtnQkFBQ2tCLE9BQU9BOztrQ0FDcEIsOERBQUNqQixpRUFBV0E7Ozs7O2tDQUNaLDhEQUFDRSxtRkFBR0E7d0JBQ0ZrQixJQUFJOzRCQUNGQyxVQUFVOzRCQUNWQyxLQUFLOzRCQUNMQyxPQUFPOzRCQUNQQyxRQUFRO3dCQUNWO2tDQUVBLDRFQUFDckIsMEZBQVVBOzRCQUNUc0IsU0FBU1YsVUFBVVAsZUFBZTs0QkFDbENrQixPQUFNOzRCQUNOTixJQUFJO2dDQUNGTyxTQUFTO2dDQUNULFdBQVc7b0NBQ1RBLFNBQVM7b0NBQ1RDLFNBQVM7Z0NBQ1g7NEJBQ0Y7c0NBRUNmLFNBQVMsdUJBQVMsOERBQUNSLHVFQUFlQTs7OztxREFBTSw4REFBQ0QsdUVBQWVBOzs7Ozs7Ozs7Ozs7Ozs7a0NBRzdELDhEQUFDTzt3QkFBVyxHQUFHQyxTQUFTOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBS2xDO0FBRUEsaUVBQWVGLEtBQUtBLEVBQUMiLCJzb3VyY2VzIjpbIi9Vc2Vycy9kYXZpZC9EZXNrdG9wL2RldmVsb3BtZW50L2F1ZGFmYWN0L3BhY2thZ2VzL3dlYi9zcmMvcGFnZXMvX2FwcC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgdXNlU3RhdGUsIHVzZU1lbW8gfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBUaGVtZVByb3ZpZGVyIH0gZnJvbSAnQG11aS9tYXRlcmlhbC9zdHlsZXMnO1xuaW1wb3J0IENzc0Jhc2VsaW5lIGZyb20gJ0BtdWkvbWF0ZXJpYWwvQ3NzQmFzZWxpbmUnO1xuaW1wb3J0IHsgY3JlYXRlQXBwVGhlbWUgfSBmcm9tICcuLi90aGVtZSc7XG5pbXBvcnQgeyBCb3gsIEljb25CdXR0b24gfSBmcm9tICdAbXVpL21hdGVyaWFsJztcbmltcG9ydCBCcmlnaHRuZXNzNEljb24gZnJvbSAnQG11aS9pY29ucy1tYXRlcmlhbC9CcmlnaHRuZXNzNCc7XG5pbXBvcnQgQnJpZ2h0bmVzczdJY29uIGZyb20gJ0BtdWkvaWNvbnMtbWF0ZXJpYWwvQnJpZ2h0bmVzczcnO1xuXG4vLyBDcmVhdGUgYSBjb250ZXh0IGZvciB0aGVtZSBtb2RlXG5pbXBvcnQgeyBjcmVhdGVDb250ZXh0IH0gZnJvbSAncmVhY3QnO1xuZXhwb3J0IGNvbnN0IENvbG9yTW9kZUNvbnRleHQgPSBjcmVhdGVDb250ZXh0KHsgXG4gIHRvZ2dsZUNvbG9yTW9kZTogKCkgPT4ge30gXG59KTtcblxuaW1wb3J0IHsgQW5hbHlzaXNQcm92aWRlciB9IGZyb20gJy4uL2NvbnRleHQvQW5hbHlzaXNDb250ZXh0JztcblxuZnVuY3Rpb24gTXlBcHAoeyBDb21wb25lbnQsIHBhZ2VQcm9wcyB9KSB7XG4gIGNvbnN0IFttb2RlLCBzZXRNb2RlXSA9IHVzZVN0YXRlPCdsaWdodCcgfCAnZGFyayc+KCdkYXJrJyk7XG4gIFxuICBjb25zdCBjb2xvck1vZGUgPSB1c2VNZW1vKFxuICAgICgpID0+ICh7XG4gICAgICB0b2dnbGVDb2xvck1vZGU6ICgpID0+IHtcbiAgICAgICAgc2V0TW9kZSgocHJldk1vZGUpID0+IChwcmV2TW9kZSA9PT0gJ2xpZ2h0JyA/ICdkYXJrJyA6ICdsaWdodCcpKTtcbiAgICAgIH0sXG4gICAgfSksXG4gICAgW11cbiAgKTtcblxuICBjb25zdCB0aGVtZSA9IHVzZU1lbW8oKCkgPT4gY3JlYXRlQXBwVGhlbWUobW9kZSksIFttb2RlXSk7XG5cbiAgcmV0dXJuIChcbiAgICA8QW5hbHlzaXNQcm92aWRlcj5cbiAgICAgIDxDb2xvck1vZGVDb250ZXh0LlByb3ZpZGVyIHZhbHVlPXtjb2xvck1vZGV9PlxuICAgICAgICA8VGhlbWVQcm92aWRlciB0aGVtZT17dGhlbWV9PlxuICAgICAgICAgIDxDc3NCYXNlbGluZSAvPlxuICAgICAgICAgIDxCb3hcbiAgICAgICAgICAgIHN4PXt7XG4gICAgICAgICAgICAgIHBvc2l0aW9uOiAnZml4ZWQnLFxuICAgICAgICAgICAgICB0b3A6IDE2LFxuICAgICAgICAgICAgICByaWdodDogMTYsXG4gICAgICAgICAgICAgIHpJbmRleDogMTAwMCxcbiAgICAgICAgICAgIH19XG4gICAgICAgICAgPlxuICAgICAgICAgICAgPEljb25CdXR0b24gXG4gICAgICAgICAgICAgIG9uQ2xpY2s9e2NvbG9yTW9kZS50b2dnbGVDb2xvck1vZGV9IFxuICAgICAgICAgICAgICBjb2xvcj1cImluaGVyaXRcIlxuICAgICAgICAgICAgICBzeD17e1xuICAgICAgICAgICAgICAgIGJnY29sb3I6ICdiYWNrZ3JvdW5kLnBhcGVyJyxcbiAgICAgICAgICAgICAgICAnJjpob3Zlcic6IHtcbiAgICAgICAgICAgICAgICAgIGJnY29sb3I6ICdiYWNrZ3JvdW5kLnBhcGVyJyxcbiAgICAgICAgICAgICAgICAgIG9wYWNpdHk6IDAuOSxcbiAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICB7bW9kZSA9PT0gJ2RhcmsnID8gPEJyaWdodG5lc3M3SWNvbiAvPiA6IDxCcmlnaHRuZXNzNEljb24gLz59XG4gICAgICAgICAgICA8L0ljb25CdXR0b24+XG4gICAgICAgICAgPC9Cb3g+XG4gICAgICAgICAgPENvbXBvbmVudCB7Li4ucGFnZVByb3BzfSAvPlxuICAgICAgICA8L1RoZW1lUHJvdmlkZXI+XG4gICAgICA8L0NvbG9yTW9kZUNvbnRleHQuUHJvdmlkZXI+XG4gICAgPC9BbmFseXNpc1Byb3ZpZGVyPlxuICApO1xufVxuXG5leHBvcnQgZGVmYXVsdCBNeUFwcDsiXSwibmFtZXMiOlsidXNlU3RhdGUiLCJ1c2VNZW1vIiwiVGhlbWVQcm92aWRlciIsIkNzc0Jhc2VsaW5lIiwiY3JlYXRlQXBwVGhlbWUiLCJCb3giLCJJY29uQnV0dG9uIiwiQnJpZ2h0bmVzczRJY29uIiwiQnJpZ2h0bmVzczdJY29uIiwiY3JlYXRlQ29udGV4dCIsIkNvbG9yTW9kZUNvbnRleHQiLCJ0b2dnbGVDb2xvck1vZGUiLCJBbmFseXNpc1Byb3ZpZGVyIiwiTXlBcHAiLCJDb21wb25lbnQiLCJwYWdlUHJvcHMiLCJtb2RlIiwic2V0TW9kZSIsImNvbG9yTW9kZSIsInByZXZNb2RlIiwidGhlbWUiLCJQcm92aWRlciIsInZhbHVlIiwic3giLCJwb3NpdGlvbiIsInRvcCIsInJpZ2h0IiwiekluZGV4Iiwib25DbGljayIsImNvbG9yIiwiYmdjb2xvciIsIm9wYWNpdHkiXSwiaWdub3JlTGlzdCI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///./src/pages/_app.tsx\n");

/***/ }),

/***/ "./src/theme/index.ts":
/*!****************************!*\
  !*** ./src/theme/index.ts ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   createAppTheme: () => (/* binding */ createAppTheme),\n/* harmony export */   theme: () => (/* binding */ theme)\n/* harmony export */ });\n/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material/styles */ \"./node_modules/@mui/material/node/styles/index.js\");\n/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material_styles__WEBPACK_IMPORTED_MODULE_0__);\n\nconst getDesignTokens = (mode)=>({\n        palette: {\n            mode,\n            ...mode === 'light' ? {\n                // Light mode - \"Disturbed\" theme\n                primary: {\n                    main: '#5c6b8a',\n                    light: '#a2b8d2',\n                    dark: '#4a5670'\n                },\n                secondary: {\n                    main: '#f07838',\n                    light: '#f5c9a8',\n                    dark: '#ba4c40'\n                },\n                background: {\n                    default: '#f5f7fa',\n                    paper: '#ffffff'\n                },\n                text: {\n                    primary: '#5c6b8a',\n                    secondary: '#ba4c40'\n                }\n            } : {\n                // Dark mode - original dark theme\n                primary: {\n                    main: '#3c3f68',\n                    light: '#4d4d80',\n                    dark: '#282c4d'\n                },\n                background: {\n                    default: '#1c1f3b',\n                    paper: '#282c4d'\n                },\n                text: {\n                    primary: '#fff',\n                    secondary: '#ba4c40'\n                }\n            }\n        },\n        components: {\n            MuiStepper: {\n                styleOverrides: {\n                    root: {\n                        backgroundColor: 'transparent',\n                        padding: 0,\n                        '& .MuiStepConnector-line': {\n                            borderColor: mode === 'light' ? '#a2b8d2' : '#606271'\n                        }\n                    }\n                }\n            },\n            MuiStepLabel: {\n                styleOverrides: {\n                    label: {\n                        color: mode === 'light' ? '#a2b8d2' : '#606271',\n                        '&.Mui-active': {\n                            color: mode === 'light' ? '#f07838' : '#ffffff'\n                        },\n                        '&.Mui-completed': {\n                            color: mode === 'light' ? '#5c6b8a' : '#3c3f68'\n                        }\n                    }\n                }\n            },\n            MuiStepIcon: {\n                styleOverrides: {\n                    root: {\n                        color: mode === 'light' ? '#a2b8d2' : '#606271',\n                        '&.Mui-active': {\n                            color: mode === 'light' ? '#f07838' : '#ffffff'\n                        },\n                        '&.Mui-completed': {\n                            color: mode === 'light' ? '#5c6b8a' : '#3c3f68'\n                        }\n                    },\n                    text: {\n                        fill: mode === 'dark' ? '#1c1f3b' : '#ffffff'\n                    }\n                }\n            },\n            MuiButton: {\n                styleOverrides: {\n                    root: {\n                        borderRadius: 8\n                    },\n                    contained: {\n                        backgroundColor: mode === 'light' ? '#5c6b8a' : '#3c3f68',\n                        '&:hover': {\n                            backgroundColor: mode === 'light' ? '#4a5670' : '#282c4d'\n                        }\n                    }\n                }\n            },\n            MuiPaper: {\n                styleOverrides: {\n                    root: {\n                        ...mode === 'light' && {\n                            boxShadow: '0 2px 4px rgba(92, 107, 138, 0.1)'\n                        }\n                    }\n                }\n            }\n        }\n    });\n// Create theme instance\nconst theme = (0,_mui_material_styles__WEBPACK_IMPORTED_MODULE_0__.createTheme)(getDesignTokens('dark')); // Default to dark mode\n// Export the theme creator function for dynamic theme switching\nconst createAppTheme = (mode)=>(0,_mui_material_styles__WEBPACK_IMPORTED_MODULE_0__.createTheme)(getDesignTokens(mode));\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvdGhlbWUvaW5kZXgudHMiLCJtYXBwaW5ncyI6Ijs7Ozs7OztBQUFpRTtBQUVqRSxNQUFNQyxrQkFBa0IsQ0FBQ0MsT0FBMEM7UUFDakVDLFNBQVM7WUFDUEQ7WUFDQSxHQUFJQSxTQUFTLFVBQ1Q7Z0JBQ0UsaUNBQWlDO2dCQUNqQ0UsU0FBUztvQkFDUEMsTUFBTTtvQkFDTkMsT0FBTztvQkFDUEMsTUFBTTtnQkFDUjtnQkFDQUMsV0FBVztvQkFDVEgsTUFBTTtvQkFDTkMsT0FBTztvQkFDUEMsTUFBTTtnQkFDUjtnQkFDQUUsWUFBWTtvQkFDVkMsU0FBUztvQkFDVEMsT0FBTztnQkFDVDtnQkFDQUMsTUFBTTtvQkFDSlIsU0FBUztvQkFDVEksV0FBVztnQkFDYjtZQUNGLElBQ0E7Z0JBQ0Usa0NBQWtDO2dCQUNsQ0osU0FBUztvQkFDUEMsTUFBTTtvQkFDTkMsT0FBTztvQkFDUEMsTUFBTTtnQkFDUjtnQkFDQUUsWUFBWTtvQkFDVkMsU0FBUztvQkFDVEMsT0FBTztnQkFDVDtnQkFDQUMsTUFBTTtvQkFDSlIsU0FBUztvQkFDVEksV0FBVztnQkFDYjtZQUNGLENBQUM7UUFDUDtRQUNBSyxZQUFZO1lBQ1ZDLFlBQVk7Z0JBQ1ZDLGdCQUFnQjtvQkFDZEMsTUFBTTt3QkFDSkMsaUJBQWlCO3dCQUNqQkMsU0FBUzt3QkFDVCw0QkFBNEI7NEJBQzFCQyxhQUFhakIsU0FBUyxVQUFVLFlBQVk7d0JBQzlDO29CQUNGO2dCQUNGO1lBQ0Y7WUFDQWtCLGNBQWM7Z0JBQ1pMLGdCQUFnQjtvQkFDZE0sT0FBTzt3QkFDTEMsT0FBT3BCLFNBQVMsVUFBVSxZQUFZO3dCQUN0QyxnQkFBZ0I7NEJBQ2RvQixPQUFPcEIsU0FBUyxVQUFVLFlBQVk7d0JBQ3hDO3dCQUNBLG1CQUFtQjs0QkFDakJvQixPQUFPcEIsU0FBUyxVQUFVLFlBQVk7d0JBQ3hDO29CQUNGO2dCQUNGO1lBQ0Y7WUFDQXFCLGFBQWE7Z0JBQ1hSLGdCQUFnQjtvQkFDZEMsTUFBTTt3QkFDSk0sT0FBT3BCLFNBQVMsVUFBVSxZQUFZO3dCQUN0QyxnQkFBZ0I7NEJBQ2RvQixPQUFPcEIsU0FBUyxVQUFVLFlBQVk7d0JBQ3hDO3dCQUNBLG1CQUFtQjs0QkFDakJvQixPQUFPcEIsU0FBUyxVQUFVLFlBQVk7d0JBQ3hDO29CQUNGO29CQUNBVSxNQUFNO3dCQUNKWSxNQUFNdEIsU0FBUyxTQUFTLFlBQVk7b0JBQ3RDO2dCQUNGO1lBQ0Y7WUFDQXVCLFdBQVc7Z0JBQ1RWLGdCQUFnQjtvQkFDZEMsTUFBTTt3QkFDSlUsY0FBYztvQkFDaEI7b0JBQ0FDLFdBQVc7d0JBQ1RWLGlCQUFpQmYsU0FBUyxVQUFVLFlBQVk7d0JBQ2hELFdBQVc7NEJBQ1RlLGlCQUFpQmYsU0FBUyxVQUFVLFlBQVk7d0JBQ2xEO29CQUNGO2dCQUNGO1lBQ0Y7WUFDQTBCLFVBQVU7Z0JBQ1JiLGdCQUFnQjtvQkFDZEMsTUFBTTt3QkFDSixHQUFJZCxTQUFTLFdBQVc7NEJBQ3RCMkIsV0FBVzt3QkFDYixDQUFDO29CQUNIO2dCQUNGO1lBQ0Y7UUFDRjtJQUNGO0FBRUEsd0JBQXdCO0FBQ2pCLE1BQU1DLFFBQVE5QixpRUFBV0EsQ0FBQ0MsZ0JBQWdCLFNBQVMsQ0FBQyx1QkFBdUI7QUFFbEYsZ0VBQWdFO0FBQ3pELE1BQU04QixpQkFBaUIsQ0FBQzdCLE9BQTJCRixpRUFBV0EsQ0FBQ0MsZ0JBQWdCQyxPQUFPIiwic291cmNlcyI6WyIvVXNlcnMvZGF2aWQvRGVza3RvcC9kZXZlbG9wbWVudC9hdWRhZmFjdC9wYWNrYWdlcy93ZWIvc3JjL3RoZW1lL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IGNyZWF0ZVRoZW1lLCBUaGVtZU9wdGlvbnMgfSBmcm9tICdAbXVpL21hdGVyaWFsL3N0eWxlcyc7XG5cbmNvbnN0IGdldERlc2lnblRva2VucyA9IChtb2RlOiAnbGlnaHQnIHwgJ2RhcmsnKTogVGhlbWVPcHRpb25zID0+ICh7XG4gIHBhbGV0dGU6IHtcbiAgICBtb2RlLFxuICAgIC4uLihtb2RlID09PSAnbGlnaHQnXG4gICAgICA/IHtcbiAgICAgICAgICAvLyBMaWdodCBtb2RlIC0gXCJEaXN0dXJiZWRcIiB0aGVtZVxuICAgICAgICAgIHByaW1hcnk6IHtcbiAgICAgICAgICAgIG1haW46ICcjNWM2YjhhJywgICAgICAvLyBXYWlrYXdhIEdyYXlcbiAgICAgICAgICAgIGxpZ2h0OiAnI2EyYjhkMicsICAgICAvLyBSb2NrIEJsdWVcbiAgICAgICAgICAgIGRhcms6ICcjNGE1NjcwJywgICAgICBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHNlY29uZGFyeToge1xuICAgICAgICAgICAgbWFpbjogJyNmMDc4MzgnLCAgICAgIC8vIEphZmZhXG4gICAgICAgICAgICBsaWdodDogJyNmNWM5YTgnLCAgICAgLy8gTWFpemVcbiAgICAgICAgICAgIGRhcms6ICcjYmE0YzQwJywgICAgICAvLyBDcmFpbFxuICAgICAgICAgIH0sXG4gICAgICAgICAgYmFja2dyb3VuZDoge1xuICAgICAgICAgICAgZGVmYXVsdDogJyNmNWY3ZmEnLCAgIFxuICAgICAgICAgICAgcGFwZXI6ICcjZmZmZmZmJywgICAgIFxuICAgICAgICAgIH0sXG4gICAgICAgICAgdGV4dDoge1xuICAgICAgICAgICAgcHJpbWFyeTogJyM1YzZiOGEnLCAgIC8vIFdhaWthd2EgR3JheVxuICAgICAgICAgICAgc2Vjb25kYXJ5OiAnI2JhNGM0MCcsICAvLyBDcmFpbFxuICAgICAgICAgIH0sXG4gICAgICAgIH1cbiAgICAgIDoge1xuICAgICAgICAgIC8vIERhcmsgbW9kZSAtIG9yaWdpbmFsIGRhcmsgdGhlbWVcbiAgICAgICAgICBwcmltYXJ5OiB7XG4gICAgICAgICAgICBtYWluOiAnIzNjM2Y2OCcsICAgICAgLy8gRmlvcmRcbiAgICAgICAgICAgIGxpZ2h0OiAnIzRkNGQ4MCcsICAgICAvLyBFYXN0IEJheVxuICAgICAgICAgICAgZGFyazogJyMyODJjNGQnLCAgICAgIC8vIE1hcnRpbmlxdWVcbiAgICAgICAgICB9LFxuICAgICAgICAgIGJhY2tncm91bmQ6IHtcbiAgICAgICAgICAgIGRlZmF1bHQ6ICcjMWMxZjNiJywgICAvLyBNaXJhZ2VcbiAgICAgICAgICAgIHBhcGVyOiAnIzI4MmM0ZCcsICAgICAvLyBNYXJ0aW5pcXVlXG4gICAgICAgICAgfSxcbiAgICAgICAgICB0ZXh0OiB7XG4gICAgICAgICAgICBwcmltYXJ5OiAnI2ZmZicsXG4gICAgICAgICAgICBzZWNvbmRhcnk6ICcjYmE0YzQwJywgIC8vIENyYWlsXG4gICAgICAgICAgfSxcbiAgICAgICAgfSksXG4gIH0sXG4gIGNvbXBvbmVudHM6IHtcbiAgICBNdWlTdGVwcGVyOiB7XG4gICAgICBzdHlsZU92ZXJyaWRlczoge1xuICAgICAgICByb290OiB7XG4gICAgICAgICAgYmFja2dyb3VuZENvbG9yOiAndHJhbnNwYXJlbnQnLFxuICAgICAgICAgIHBhZGRpbmc6IDAsXG4gICAgICAgICAgJyYgLk11aVN0ZXBDb25uZWN0b3ItbGluZSc6IHtcbiAgICAgICAgICAgIGJvcmRlckNvbG9yOiBtb2RlID09PSAnbGlnaHQnID8gJyNhMmI4ZDInIDogJyM2MDYyNzEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIH0sXG4gICAgICB9LFxuICAgIH0sXG4gICAgTXVpU3RlcExhYmVsOiB7XG4gICAgICBzdHlsZU92ZXJyaWRlczoge1xuICAgICAgICBsYWJlbDoge1xuICAgICAgICAgIGNvbG9yOiBtb2RlID09PSAnbGlnaHQnID8gJyNhMmI4ZDInIDogJyM2MDYyNzEnLFxuICAgICAgICAgICcmLk11aS1hY3RpdmUnOiB7XG4gICAgICAgICAgICBjb2xvcjogbW9kZSA9PT0gJ2xpZ2h0JyA/ICcjZjA3ODM4JyA6ICcjZmZmZmZmJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgICcmLk11aS1jb21wbGV0ZWQnOiB7XG4gICAgICAgICAgICBjb2xvcjogbW9kZSA9PT0gJ2xpZ2h0JyA/ICcjNWM2YjhhJyA6ICcjM2MzZjY4JyxcbiAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgfSxcbiAgICB9LFxuICAgIE11aVN0ZXBJY29uOiB7XG4gICAgICBzdHlsZU92ZXJyaWRlczoge1xuICAgICAgICByb290OiB7XG4gICAgICAgICAgY29sb3I6IG1vZGUgPT09ICdsaWdodCcgPyAnI2EyYjhkMicgOiAnIzYwNjI3MScsXG4gICAgICAgICAgJyYuTXVpLWFjdGl2ZSc6IHtcbiAgICAgICAgICAgIGNvbG9yOiBtb2RlID09PSAnbGlnaHQnID8gJyNmMDc4MzgnIDogJyNmZmZmZmYnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAgJyYuTXVpLWNvbXBsZXRlZCc6IHtcbiAgICAgICAgICAgIGNvbG9yOiBtb2RlID09PSAnbGlnaHQnID8gJyM1YzZiOGEnIDogJyMzYzNmNjgnLFxuICAgICAgICAgIH0sXG4gICAgICAgIH0sXG4gICAgICAgIHRleHQ6IHtcbiAgICAgICAgICBmaWxsOiBtb2RlID09PSAnZGFyaycgPyAnIzFjMWYzYicgOiAnI2ZmZmZmZicsXG4gICAgICAgIH0sXG4gICAgICB9LFxuICAgIH0sXG4gICAgTXVpQnV0dG9uOiB7XG4gICAgICBzdHlsZU92ZXJyaWRlczoge1xuICAgICAgICByb290OiB7XG4gICAgICAgICAgYm9yZGVyUmFkaXVzOiA4LFxuICAgICAgICB9LFxuICAgICAgICBjb250YWluZWQ6IHtcbiAgICAgICAgICBiYWNrZ3JvdW5kQ29sb3I6IG1vZGUgPT09ICdsaWdodCcgPyAnIzVjNmI4YScgOiAnIzNjM2Y2OCcsXG4gICAgICAgICAgJyY6aG92ZXInOiB7XG4gICAgICAgICAgICBiYWNrZ3JvdW5kQ29sb3I6IG1vZGUgPT09ICdsaWdodCcgPyAnIzRhNTY3MCcgOiAnIzI4MmM0ZCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSxcbiAgICBNdWlQYXBlcjoge1xuICAgICAgc3R5bGVPdmVycmlkZXM6IHtcbiAgICAgICAgcm9vdDoge1xuICAgICAgICAgIC4uLihtb2RlID09PSAnbGlnaHQnICYmIHtcbiAgICAgICAgICAgIGJveFNoYWRvdzogJzAgMnB4IDRweCByZ2JhKDkyLCAxMDcsIDEzOCwgMC4xKScsXG4gICAgICAgICAgfSksXG4gICAgICAgIH0sXG4gICAgICB9LFxuICAgIH0sXG4gIH0sXG59KTtcblxuLy8gQ3JlYXRlIHRoZW1lIGluc3RhbmNlXG5leHBvcnQgY29uc3QgdGhlbWUgPSBjcmVhdGVUaGVtZShnZXREZXNpZ25Ub2tlbnMoJ2RhcmsnKSk7IC8vIERlZmF1bHQgdG8gZGFyayBtb2RlXG5cbi8vIEV4cG9ydCB0aGUgdGhlbWUgY3JlYXRvciBmdW5jdGlvbiBmb3IgZHluYW1pYyB0aGVtZSBzd2l0Y2hpbmdcbmV4cG9ydCBjb25zdCBjcmVhdGVBcHBUaGVtZSA9IChtb2RlOiAnbGlnaHQnIHwgJ2RhcmsnKSA9PiBjcmVhdGVUaGVtZShnZXREZXNpZ25Ub2tlbnMobW9kZSkpO1xuIl0sIm5hbWVzIjpbImNyZWF0ZVRoZW1lIiwiZ2V0RGVzaWduVG9rZW5zIiwibW9kZSIsInBhbGV0dGUiLCJwcmltYXJ5IiwibWFpbiIsImxpZ2h0IiwiZGFyayIsInNlY29uZGFyeSIsImJhY2tncm91bmQiLCJkZWZhdWx0IiwicGFwZXIiLCJ0ZXh0IiwiY29tcG9uZW50cyIsIk11aVN0ZXBwZXIiLCJzdHlsZU92ZXJyaWRlcyIsInJvb3QiLCJiYWNrZ3JvdW5kQ29sb3IiLCJwYWRkaW5nIiwiYm9yZGVyQ29sb3IiLCJNdWlTdGVwTGFiZWwiLCJsYWJlbCIsImNvbG9yIiwiTXVpU3RlcEljb24iLCJmaWxsIiwiTXVpQnV0dG9uIiwiYm9yZGVyUmFkaXVzIiwiY29udGFpbmVkIiwiTXVpUGFwZXIiLCJib3hTaGFkb3ciLCJ0aGVtZSIsImNyZWF0ZUFwcFRoZW1lIl0sImlnbm9yZUxpc3QiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./src/theme/index.ts\n");

/***/ }),

/***/ "@mui/system":
/*!******************************!*\
  !*** external "@mui/system" ***!
  \******************************/
/***/ ((module) => {

module.exports = require("@mui/system");

/***/ }),

/***/ "@mui/system/DefaultPropsProvider":
/*!***************************************************!*\
  !*** external "@mui/system/DefaultPropsProvider" ***!
  \***************************************************/
/***/ ((module) => {

module.exports = require("@mui/system/DefaultPropsProvider");

/***/ }),

/***/ "@mui/system/InitColorSchemeScript":
/*!****************************************************!*\
  !*** external "@mui/system/InitColorSchemeScript" ***!
  \****************************************************/
/***/ ((module) => {

module.exports = require("@mui/system/InitColorSchemeScript");

/***/ }),

/***/ "@mui/system/colorManipulator":
/*!***********************************************!*\
  !*** external "@mui/system/colorManipulator" ***!
  \***********************************************/
/***/ ((module) => {

module.exports = require("@mui/system/colorManipulator");

/***/ }),

/***/ "@mui/system/createBreakpoints":
/*!************************************************!*\
  !*** external "@mui/system/createBreakpoints" ***!
  \************************************************/
/***/ ((module) => {

module.exports = require("@mui/system/createBreakpoints");

/***/ }),

/***/ "@mui/system/createStyled":
/*!*******************************************!*\
  !*** external "@mui/system/createStyled" ***!
  \*******************************************/
/***/ ((module) => {

module.exports = require("@mui/system/createStyled");

/***/ }),

/***/ "@mui/system/createTheme":
/*!******************************************!*\
  !*** external "@mui/system/createTheme" ***!
  \******************************************/
/***/ ((module) => {

module.exports = require("@mui/system/createTheme");

/***/ }),

/***/ "@mui/system/cssVars":
/*!**************************************!*\
  !*** external "@mui/system/cssVars" ***!
  \**************************************/
/***/ ((module) => {

module.exports = require("@mui/system/cssVars");

/***/ }),

/***/ "@mui/system/spacing":
/*!**************************************!*\
  !*** external "@mui/system/spacing" ***!
  \**************************************/
/***/ ((module) => {

module.exports = require("@mui/system/spacing");

/***/ }),

/***/ "@mui/system/styleFunctionSx":
/*!**********************************************!*\
  !*** external "@mui/system/styleFunctionSx" ***!
  \**********************************************/
/***/ ((module) => {

module.exports = require("@mui/system/styleFunctionSx");

/***/ }),

/***/ "@mui/system/useThemeProps":
/*!********************************************!*\
  !*** external "@mui/system/useThemeProps" ***!
  \********************************************/
/***/ ((module) => {

module.exports = require("@mui/system/useThemeProps");

/***/ }),

/***/ "@mui/utils":
/*!*****************************!*\
  !*** external "@mui/utils" ***!
  \*****************************/
/***/ ((module) => {

module.exports = require("@mui/utils");

/***/ }),

/***/ "@mui/utils/capitalize":
/*!****************************************!*\
  !*** external "@mui/utils/capitalize" ***!
  \****************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/capitalize");

/***/ }),

/***/ "@mui/utils/chainPropTypes":
/*!********************************************!*\
  !*** external "@mui/utils/chainPropTypes" ***!
  \********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/chainPropTypes");

/***/ }),

/***/ "@mui/utils/composeClasses":
/*!********************************************!*\
  !*** external "@mui/utils/composeClasses" ***!
  \********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/composeClasses");

/***/ }),

/***/ "@mui/utils/createChainedFunction":
/*!***************************************************!*\
  !*** external "@mui/utils/createChainedFunction" ***!
  \***************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/createChainedFunction");

/***/ }),

/***/ "@mui/utils/debounce":
/*!**************************************!*\
  !*** external "@mui/utils/debounce" ***!
  \**************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/debounce");

/***/ }),

/***/ "@mui/utils/deepmerge":
/*!***************************************!*\
  !*** external "@mui/utils/deepmerge" ***!
  \***************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/deepmerge");

/***/ }),

/***/ "@mui/utils/deprecatedPropType":
/*!************************************************!*\
  !*** external "@mui/utils/deprecatedPropType" ***!
  \************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/deprecatedPropType");

/***/ }),

/***/ "@mui/utils/elementTypeAcceptingRef":
/*!*****************************************************!*\
  !*** external "@mui/utils/elementTypeAcceptingRef" ***!
  \*****************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/elementTypeAcceptingRef");

/***/ }),

/***/ "@mui/utils/formatMuiErrorMessage":
/*!***************************************************!*\
  !*** external "@mui/utils/formatMuiErrorMessage" ***!
  \***************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/formatMuiErrorMessage");

/***/ }),

/***/ "@mui/utils/generateUtilityClass":
/*!**************************************************!*\
  !*** external "@mui/utils/generateUtilityClass" ***!
  \**************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/generateUtilityClass");

/***/ }),

/***/ "@mui/utils/generateUtilityClasses":
/*!****************************************************!*\
  !*** external "@mui/utils/generateUtilityClasses" ***!
  \****************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/generateUtilityClasses");

/***/ }),

/***/ "@mui/utils/isFocusVisible":
/*!********************************************!*\
  !*** external "@mui/utils/isFocusVisible" ***!
  \********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/isFocusVisible");

/***/ }),

/***/ "@mui/utils/isMuiElement":
/*!******************************************!*\
  !*** external "@mui/utils/isMuiElement" ***!
  \******************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/isMuiElement");

/***/ }),

/***/ "@mui/utils/ownerDocument":
/*!*******************************************!*\
  !*** external "@mui/utils/ownerDocument" ***!
  \*******************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/ownerDocument");

/***/ }),

/***/ "@mui/utils/ownerWindow":
/*!*****************************************!*\
  !*** external "@mui/utils/ownerWindow" ***!
  \*****************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/ownerWindow");

/***/ }),

/***/ "@mui/utils/refType":
/*!*************************************!*\
  !*** external "@mui/utils/refType" ***!
  \*************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/refType");

/***/ }),

/***/ "@mui/utils/requirePropFactory":
/*!************************************************!*\
  !*** external "@mui/utils/requirePropFactory" ***!
  \************************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/requirePropFactory");

/***/ }),

/***/ "@mui/utils/setRef":
/*!************************************!*\
  !*** external "@mui/utils/setRef" ***!
  \************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/setRef");

/***/ }),

/***/ "@mui/utils/unsupportedProp":
/*!*********************************************!*\
  !*** external "@mui/utils/unsupportedProp" ***!
  \*********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/unsupportedProp");

/***/ }),

/***/ "@mui/utils/useControlled":
/*!*******************************************!*\
  !*** external "@mui/utils/useControlled" ***!
  \*******************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useControlled");

/***/ }),

/***/ "@mui/utils/useEnhancedEffect":
/*!***********************************************!*\
  !*** external "@mui/utils/useEnhancedEffect" ***!
  \***********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useEnhancedEffect");

/***/ }),

/***/ "@mui/utils/useEventCallback":
/*!**********************************************!*\
  !*** external "@mui/utils/useEventCallback" ***!
  \**********************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useEventCallback");

/***/ }),

/***/ "@mui/utils/useForkRef":
/*!****************************************!*\
  !*** external "@mui/utils/useForkRef" ***!
  \****************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useForkRef");

/***/ }),

/***/ "@mui/utils/useId":
/*!***********************************!*\
  !*** external "@mui/utils/useId" ***!
  \***********************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useId");

/***/ }),

/***/ "@mui/utils/useLazyRef":
/*!****************************************!*\
  !*** external "@mui/utils/useLazyRef" ***!
  \****************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useLazyRef");

/***/ }),

/***/ "@mui/utils/useTimeout":
/*!****************************************!*\
  !*** external "@mui/utils/useTimeout" ***!
  \****************************************/
/***/ ((module) => {

module.exports = require("@mui/utils/useTimeout");

/***/ }),

/***/ "clsx?ce27":
/*!***********************!*\
  !*** external "clsx" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("clsx");

/***/ }),

/***/ "prop-types":
/*!*****************************!*\
  !*** external "prop-types" ***!
  \*****************************/
/***/ ((module) => {

module.exports = require("prop-types");

/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/***/ ((module) => {

module.exports = require("react");

/***/ }),

/***/ "react-transition-group":
/*!*****************************************!*\
  !*** external "react-transition-group" ***!
  \*****************************************/
/***/ ((module) => {

module.exports = require("react-transition-group");

/***/ }),

/***/ "react/jsx-dev-runtime":
/*!****************************************!*\
  !*** external "react/jsx-dev-runtime" ***!
  \****************************************/
/***/ ((module) => {

module.exports = require("react/jsx-dev-runtime");

/***/ }),

/***/ "react/jsx-runtime":
/*!************************************!*\
  !*** external "react/jsx-runtime" ***!
  \************************************/
/***/ ((module) => {

module.exports = require("react/jsx-runtime");

/***/ }),

/***/ "clsx?9dfb":
/*!***********************!*\
  !*** external "clsx" ***!
  \***********************/
/***/ ((module) => {

module.exports = import("clsx");;

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, ["vendor-chunks/@mui","vendor-chunks/@babel"], () => (__webpack_exec__("./src/pages/_app.tsx")));
module.exports = __webpack_exports__;

})();