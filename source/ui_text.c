#include "ui_text.h"

/* Compiled into the 3DS binary, so drawing never reads text from the SD card. */
const char *const uiStrings[UI_STRING_COUNT] = {
    [UI_VA_11_HALL_A] = "VA-11 HALL-A",
    [UI_DEN_5_0_8_0] = "ДЕНЬ 5 / 0.9.0",
    [UI_DEN_4_0_8_0] = "ДЕНЬ 4 / 0.9.0",
    [UI_DEN_3_0_8_0] = "ДЕНЬ 3 / 0.9.0",
    [UI_DEN_2_0_8_0] = "ДЕНЬ 2 / 0.9.0",
    [UI_DEN_1_0_8_0] = "ДЕНЬ 1 / 0.9.0",
    [UI_NOVOSTI] = "НОВОСТИ",
    [UI_DZHILL] = "ДЖИЛЛ",
    [UI_EMPTY] = "",
    [UI_APLODISM] = "Аплодисм.",
    [UI_DA_A_A] = "Да-а-а!",
    [UI_BU_U] = "Бу-у!",
    [UI_NET] = "Нет!",
    [UI_HA_HA] = "Ха-ха!",
    [UI_O_O] = "О-о...",
    [UI_CHAT_STRIMA] = "ЧАТ СТРИМА",
    [UI_A] = "A >>",
    [UI_ZAKAZ] = "ЗАКАЗ",
    [UI_NAPITOK_2_2_X_PODAT_OBA] = "Напиток 2/2. X: подать оба",
    [UI_NAPITOK_1_2_X_OTLOZHIT_V_SLOT] = "Напиток 1/2. X: отложить в слот",
    [UI_Y_RETSEPT_A_SHEYKER_X_PODAT] = "Y: рецепт   A: шейкер   X: подать",
    [UI_B_SBROS_L_LD_R_VYDERZHKA] = "B: сброс   L: лёд   R: выдержка",
    [UI_GAME_OVER] = "GAME OVER",
    [UI_DANA_OTPRAVILA_DZHILL_DOMOY] = "Дана отправила Джилл домой.",
    [UI_A_ZAGRUZIT_NACHAT_ZANOVO] = "A: загрузить / начать заново",
    [UI_B_GLAVNOE_MENYU] = "B: главное меню",
    [UI_PERERYV] = "ПЕРЕРЫВ",
    [UI_VREMYA_NEMNOGO_OTDOHNUT] = "Время немного отдохнуть.",
    [UI_A_PRODOLZHIT_SMENU] = "A: продолжить смену",
    [UI_PYATYY_DEN_ZAVERSHN] = "ПЯТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_CHETVRTYY_DEN_ZAVERSHN] = "ЧЕТВЁРТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_TRETIY_DEN_ZAVERSHN] = "ТРЕТИЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_VTOROY_DEN_ZAVERSHN] = "ВТОРОЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_PERVYY_DEN_ZAVERSHN] = "ПЕРВЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_VYRUCHKA] = "Выручка:",
    [UI_CHAEVYE] = "Чаевые:",
    [UI_OSHIBKI] = "Ошибки:",
    [UI_ZARABOTOK] = "Заработок:",
    [UI_A_DOMOY_DEN_5_START_VYHOD] = "A: домой, день 5   START: выход",
    [UI_A_DOMOY_DEN_4_START_VYHOD] = "A: домой, день 4   START: выход",
    [UI_A_DOMOY_DEN_3_START_VYHOD] = "A: домой, день 3   START: выход",
    [UI_A_DOMOY_DEN_2_START_VYHOD] = "A: домой, день 2   START: выход",
    [UI_SELECT_MENYU_START_VYHOD] = "SELECT: меню   START: выход",
    [UI_OSHIBKA_PEREHODA_SELECT_MENYU] = "Ошибка перехода. SELECT: меню",
    [UI_SMENA_OKONCHENA_DOSROCHNO] = "СМЕНА ОКОНЧЕНА ДОСРОЧНО",
    [UI_POSLEDNIY_SEYV_SOHRANN] = "Последний сейв сохранён.",
    [UI_A_ZAGRUZIT_SOHRANENIE] = "A: загрузить сохранение",
    [UI_BEZ_SEYVA_NOVYY_PERVYY_DEN] = "Без сейва: новый первый день.",
    [UI_START_VYHOD] = "START: выход",
    [UI_BAR_OBUCHENIE] = "БАР / ОБУЧЕНИЕ",
    [UI_BAR_DEN_5] = "БАР / ДЕНЬ 5",
    [UI_BAR_DEN_4] = "БАР / ДЕНЬ 4",
    [UI_BAR_DEN_3] = "БАР / ДЕНЬ 3",
    [UI_BAR_DEN_2] = "БАР / ДЕНЬ 2",
    [UI_BAR_DEN_1] = "БАР / ДЕНЬ 1",
    [UI_VZBOLTANO_A_OSTANOVIT] = "Взболтано! A: остановить",
    [UI_SMESHIVAEM_A_OSTANOVIT] = "Смешиваем... A: остановить",
    [UI_NEUDACHNYY_KOKTEYL_B_SBROS] = "Неудачный коктейль: B сброс",
    [UI_DOBAV_INGREDIENTY_Y_RETSEPT] = "Добавь ингредиенты. Y: рецепт",
    [UI_A_CHITAT_DALSHE_Y_RETSEPTY] = "A: читать дальше   Y: рецепты",
    [UI_ADELGID] = "Адельгид",
    [UI_BRONSON_EKSTRAKT] = "Бронсон-экстракт",
    [UI_POROSHKOVAYA_DELTA] = "Порошковая дельта",
    [UI_FLANERGID] = "Фланергид",
    [UI_KARMOTRIN] = "Кармотрин",
    [UI_EMPTY_2] = "-",
    [UI_EMPTY_3] = "+",
    [UI_L_LD_DA] = "L: Лёд [ДА]",
    [UI_L_LD_NET] = "L: Лёд [нет]",
    [UI_R_VYDERZHKA_DA] = "R: Выдержка [ДА]",
    [UI_R_VYDERZHKA] = "R: Выдержка [-]",
    [UI_B_SBROS] = "B: Сброс",
    [UI_A_STOP] = "A: Стоп",
    [UI_A_SHEYKER] = "A: Шейкер",
    [UI_X_PODAT] = "X: Подать",
    [UI_ZVUK_VKLYUCHN] = "Звук: включён",
    [UI_ZVUK_NET_PCM] = "Звук: нет PCM",
    [UI_ZVUK_NET_DSP] = "Звук: нет DSP",
    [UI_OSHIBKA_ZAPISI_SD] = "Ошибка записи SD!",
    [UI_RETSEPTY_L_R] = "РЕЦЕПТЫ   < L / R >",
    [UI_GOTOVYY_NAPITOK_IZ_BUTYLKI] = "Готовый напиток из бутылки.",
    [UI_SHEYKER_NE_NUZHEN] = "Шейкер не нужен.",
    [UI_POKA_NEDOSTUPNO] = "Пока недоступно.",
    [UI_A_NALIT_X_ZATEM_PODAT] = "A: налить   X: затем подать",
    [UI_NALIVAT_MOZHNO_PRI_ZAKAZE] = "Наливать можно при заказе.",
    [UI_DOSTUPEN_BEZ_POKUPKI_V_BETE] = "Доступен без покупки в бете.",
    [UI_KLASSICHESKIY_S_ALKOGOLEM] = "Классический, с алкоголем.",
    [UI_DOSTUPNOST_ZAVISIT_OT_STELLY] = "Доступность зависит от Стеллы.",
    [UI_PO_VKUSU] = "по вкусу",
    [UI_LD_DA] = "Лёд: да",
    [UI_LD_NET] = "Лёд: нет",
    [UI_VYDERZHKA_DA] = "Выдержка: да",
    [UI_VYDERZHKA_NET] = "Выдержка: нет",
    [UI_VZBOLTAT_5_SEKUND_I_DOLSHE] = "Взболтать: 5 секунд и дольше.",
    [UI_SMESHAT_MENEE_5_SEKUND] = "Смешать: менее 5 секунд.",
    [UI_UZHE_BOLSHOY_MAKSIMUM_20_CHASTEY] = "Уже большой. Максимум 20 частей.",
    [UI_BOLSHOY_UDVOY_MAKSIMUM_20] = "Большой: удвой. Максимум 20.",
    [UI_SLADKIY] = "Сладкий",
    [UI_GORKIY] = "Горький",
    [UI_OSTRYY] = "Острый",
    [UI_GAZOVYY] = "Газовый",
    [UI_KISLYY] = "Кислый",
    [UI_IZYSKANNYY] = "Изысканный",
    [UI_ZHENSTVENNYY] = "Женственный",
    [UI_MUZHESTVENNYY] = "Мужественный",
    [UI_REKLAMNYY_PROMO] = "Рекламный (Promo)",
    [UI_KLASSICHESKIY] = "Классический",
    [UI_Y_B_ZAKRYT_L_R_LISTAT] = "Y / B: закрыть   L/R: листать",
    [UI_PAUZA] = "ПАУЗА",
    [UI_A_GLAVNOE_MENYU] = "A: главное меню",
    [UI_A_SOHRANIT_I_OTKRYT_MENYU] = "A: сохранить и открыть меню",
    [UI_B_VERNUTSYA_K_IGRE] = "B: вернуться к игре",
    [UI_X_VYBRAT_MUZYKU] = "X: выбрать музыку",
    [UI_MAGAZIN_UKRASHENIYA_DLYA_DOMA] = "МАГАЗИН / УКРАШЕНИЯ ДЛЯ ДОМА",
    [UI_KOSHELK] = "Кошелёк:",
    [UI_TSENA] = "Цена:",
    [UI_KUPIT_A_DA_B_OTMENA] = "Купить? A: да / B: отмена",
    [UI_KUPLENO_SOHRANIS_DOMA] = "Куплено. Сохранись дома.",
    [UI_NEDOSTATOCHNO_DENEG] = "Недостаточно денег.",
    [UI_UZHE_KUPLENO] = "Уже куплено.",
    [UI_A_KASANIE_VYBRAT_POKUPKU] = "A / касание: выбрать покупку",
    [UI_B_DOMOY_STRANITSA] = "B: домой  </>: страница",
    [UI_MUZYKALNYY_AVTOMAT] = "МУЗЫКАЛЬНЫЙ АВТОМАТ",
    [UI_VYBERI_MUZYKU_PERED_SMENOY] = "Выбери музыку перед сменой.",
    [UI_MUZYKA_DLYA_ETOY_SMENY] = "Музыка для этой смены",
    [UI_SEYCHAS_VYBRANO] = "Сейчас выбрано:",
    [UI_VYBRANNYY_TREK_IGRAET_PO_KRUGU] = "Выбранный трек играет по кругу.",
    [UI_VVERH_VNIZ_TREK_STRANITSA] = "ВВЕРХ/ВНИЗ: трек  </>: страница",
    [UI_A_KASANIE_IGRAT] = "A / касание: играть",
    [UI_B_OSTAVIT_TEKUSCHIY_TREK] = "B: оставить текущий трек",
    [UI_VA_11_HALL_A_3DS] = "VA-11 HALL-A / 3DS",
    [UI_ORIGINAL_GAME_DEVELOPED_BY] = "Original game developed by",
    [UI_SUKEBAN_GAMES] = "Sukeban Games",
    [UI_MUSIC_BY_GAROAD] = "Music by Garoad",
    [UI_PUBLISHED_BY_YSBRYD_GAMES] = "Published by Ysbryd Games",
    [UI_UNOFFICIAL_FAN_MADE_PORT] = "Unofficial fan-made port",
    [UI_BUILD_WITH_NEUMIRAIE] = "build with neumiraie",
    [UI_NOT_AFFILIATED_WITH_OR_ENDORSED] = "Not affiliated with or endorsed",
    [UI_BY_THE_ORIGINAL_CREATORS] = "by the original creators.",
    [UI_A_TOUCH_CONTINUE] = "A / touch: continue",
    [UI_RUSSKIY_PEREVOD] = "РУССКИЙ ПЕРЕВОД",
    [UI_V_PORTE_ISPOLZUETSYA] = "В порте используется",
    [UI_NEOFITSIALNYY_RUSSKIY_PEREVOD] = "неофициальный русский перевод.",
    [UI_ISTOCHNIK_PEREVODA] = "Источник перевода:",
    [UI_HTTPS_KOSHK_SBS] = "https://koshk.sbs/",
    [UI_SPASIBO_KOMANDE_PEREVODA] = "Спасибо команде перевода!",
    [UI_PEREVOD_SOZDAN_FANATAMI] = "Перевод создан фанатами",
    [UI_I_NE_YAVLYAETSYA_OFITSIALNOY] = "и не является официальной",
    [UI_LOKALIZATSIEY_SUKEBAN_GAMES] = "локализацией Sukeban Games.",
    [UI_A_KASANIE_GLAVNOE_MENYU] = "A / касание: главное меню",
    [UI_VA_11_HALL_A_NINTENDO_3DS] = "VA-11 HALL-A / NINTENDO 3DS",
    [UI_TEST_DNI_1_5_KOSHELK_20000] = "ТЕСТ: дни 1-6 / кошелёк $20000",
    [UI_OTDELNOE_TESTOVOE_SOHRANENIE] = "Отдельное тестовое сохранение",
    [UI_KVARTIRA_DZHILL_DEN_5] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 5",
    [UI_KVARTIRA_DZHILL_DEN_4] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 4",
    [UI_KVARTIRA_DZHILL_DEN_3] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 3",
    [UI_KVARTIRA_DZHILL_DEN_2] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 2",
    [UI_KVARTIRA_DZHILL_DEN_1] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 1",
    [UI_DOPOLNENNAYA_PRAVDA] = "ДОПОЛНЕННАЯ ПРАВДА",
    [UI_DANGER_U] = "DANGER/U/",
    [UI_BLOG_KIRY_MIKI] = "БЛОГ КИРЫ МИКИ",
    [UI_VVERH] = "ВВЕРХ",
    [UI_VNIZ] = "ВНИЗ",
    [UI_B_NAZAD_VVERH_VNIZ_LISTAT] = "B: назад   вверх/вниз: листать",
    [UI_UPRAVLENIE] = "УПРАВЛЕНИЕ",
    [UI_A_DIALOG_SHEYKER_NX_PODAT_B_SBROS_NY_RETSEPTY_L_R_LD] = "A: диалог / шейкер\nX: подать   B: сброс\nY: рецепты   L/R: лёд/выдержка\nКрестовина: ингредиенты\nSELECT: пауза и главное меню\nSTART: сохранить и выйти",
    [UI_SMESHAT_MENEE_5_SEKUND_NVZBOLTAT_OT_5_SEKUND_NAVTOSE] = "Смешать: менее 5 секунд.\nВзболтать: от 5 секунд.\nАвтосейв: в конце дня.",
    [UI_A_B_NAZAD] = "A / B: назад",
    [UI_VA_11_HALL_A_3DS_0_8_0] = "VA-11 HALL-A / 3DS 0.9.0",
    [UI_PRODOLZHIT] = "Продолжить",
    [UI_PRODOLZHIT_NET_SOHRANENIYA] = "Продолжить (нет сохранения)",
    [UI_NOVAYA_IGRA] = "Новая игра",
    [UI_UPRAVLENIE_2] = "Управление",
    [UI_VYHOD] = "Выход",
    [UI_VA_11_HALL_A_0_8_0_TEST] = "VA-11 HALL-A / 0.9.0 TEST",
    [UI_TEST_VYBRAT_DEN] = "Тест: выбрать день",
    [UI_TEST_KVARTIRA_PERED_SMENOY] = "ТЕСТ: ВЫБРАТЬ ДЕНЬ",
    [UI_DEN_1] = "День 1",
    [UI_DEN_2] = "День 2",
    [UI_DEN_3] = "День 3",
    [UI_DEN_4] = "День 4",
    [UI_DEN_5] = "День 5",
    [UI_NOVAYA_IGRA_2] = "НОВАЯ ИГРА",
    [UI_S_OBUCHENIEM] = "С обучением",
    [UI_SRAZU_PERVYY_DEN] = "Сразу первый день",
    [UI_OTMENA] = "Отмена",
    [UI_DOM_17_DEKABRYA] = "ДОМ / 17 ДЕКАБРЯ",
    [UI_DOM_16_DEKABRYA] = "ДОМ / 16 ДЕКАБРЯ",
    [UI_DOM_15_DEKABRYA] = "ДОМ / 15 ДЕКАБРЯ",
    [UI_DOM_14_DEKABRYA] = "ДОМ / 14 ДЕКАБРЯ",
    [UI_DOM_13_DEKABRYA] = "ДОМ / 13 ДЕКАБРЯ",
    [UI_TELEFON] = "Телефон",
    [UI_NA_RABOTU] = "На работу",
    [UI_SOHRANIT] = "Сохранить",
    [UI_MAGAZIN] = "Магазин",
    [UI_TELEFON_2] = "ТЕЛЕФОН",
    [UI_DOPOLNENNAYA_PRAVDA_2] = "Дополненная правда",
    [UI_DANGER_U_2] = "danger/u/",
    [UI_BLOG_KIRY_MIKI_2] = "Блог Киры Мики",
    [UI_MASSOVAYA_EMIGRATSIYA] = "Массовая эмиграция",
    [UI_NOVAYA_UGROZA_VANDERLENDERY] = "Новая угроза: вандерлендеры",
    [UI_KIBORG_NA_KABLUKAH] = "Киборг на каблуках",
    [UI_KONTSERT_MIKI] = "Концерт Мики",
    [UI_POGOVORIM_OB_ALICE_RABBIT] = "Поговорим об Alice_Rabbit",
    [UI_KONTSERT_MIKI_2] = "Концерт Мики 2",
    [UI_KAK_YA_OTDYHAYU] = "Как я отдыхаю",
    [UI_KONTSERT_POD_KUPOLOM] = "Концерт под куполом!",
    [UI_SPASIBO_GLITCH_SITI] = "Спасибо, Глитч-Сити!",
    [UI_KIRA_MIKI] = "КИРА МИКИ",
    [UI_NOVOSTI_16_DEKABRYA] = "Новости / 16 декабря",
    [UI_VTORAYA_STATYA] = "Вторая статья",
    [UI_TRETYA_STATYA] = "Третья статья",
    [UI_NOVOSTI_15_DEKABRYA] = "Новости / 15 декабря",
    [UI_MESTNAYA_GEROINYA] = "Местная героиня",
    [UI_70_NASHIH_CHITATELEY] = "70% наших читателей...",
    [UI_BESPORYADKI_USILIVAYUTSYA] = "Беспорядки усиливаются",
    [UI_KEM_MOZHET_BYT_ALICE_RABBIT] = "Кем может быть Alice_Rabbit?",
    [UI_LECHENIE_TOKIYSKOGO_GRIPPA] = "Лечение токийского гриппа",
    [UI_NOVOSTI_17_DEKABRYA] = "Новости / 17 декабря",
    [UI_TEKUSCHIY_PROGRESS_BUDET_ZAMENN] = "Текущий прогресс будет заменён.",
    [UI_SOHRANENIE_OTPRAVLENO_NA_SD] = "Сохранение отправлено на SD.",
    [UI_A_VYBRAT_B_NAZAD] = "A: выбрать   B: назад",
    [UI_DAY6_BADGE] = "ДЕНЬ 6 / 0.9.0",
    [UI_DAY6_COMPLETED] = "ВЫХОДНОЙ ЗАВЕРШЁН",
    [UI_DAY6_NEXT] = "A: домой, день 6   START: выход",
    [UI_DAY6_SCENE] = "ДОМ / ВЫХОДНОЙ",
    [UI_DAY6_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 6",
    [UI_DAY6_DATE] = "ДОМ / 18 ДЕКАБРЯ",
    [UI_DAY6_BEER_LABEL] = "Выпито банок:",
    [UI_DAY6_DRINK_HINT] = "Y: выпить пиво (до 12)",
    [UI_DAY6_DIALOGUE_HINT] = "A: дальше   Y: пиво",
    [UI_DAY6_NO_SHIFT] = "Сегодня бар был закрыт.",
    [UI_DAY6_FINISH_HINT] = "SELECT: меню   START: выход",
    [UI_DAY6_TEST_LABEL] = "День 6",
    [UI_DAY6_NEWS_TITLE] = "Новости / 18 декабря",
};

static const UiStringId dayBadges[]={UI_DEN_1_0_8_0,UI_DEN_2_0_8_0,UI_DEN_3_0_8_0,UI_DEN_4_0_8_0,UI_DEN_5_0_8_0,UI_DAY6_BADGE};
static const UiStringId dayCompleted[]={UI_PERVYY_DEN_ZAVERSHN,UI_VTOROY_DEN_ZAVERSHN,UI_TRETIY_DEN_ZAVERSHN,UI_CHETVRTYY_DEN_ZAVERSHN,UI_PYATYY_DEN_ZAVERSHN,UI_DAY6_COMPLETED};
static const UiStringId nextDayHints[]={UI_A_DOMOY_DEN_2_START_VYHOD,UI_A_DOMOY_DEN_3_START_VYHOD,UI_A_DOMOY_DEN_4_START_VYHOD,UI_A_DOMOY_DEN_5_START_VYHOD,UI_DAY6_NEXT,UI_DAY6_FINISH_HINT};
static const UiStringId barHeadings[]={UI_BAR_DEN_1,UI_BAR_DEN_2,UI_BAR_DEN_3,UI_BAR_DEN_4,UI_BAR_DEN_5,UI_DAY6_SCENE};
static const UiStringId apartmentHeadings[]={UI_KVARTIRA_DZHILL_DEN_1,UI_KVARTIRA_DZHILL_DEN_2,UI_KVARTIRA_DZHILL_DEN_3,UI_KVARTIRA_DZHILL_DEN_4,UI_KVARTIRA_DZHILL_DEN_5,UI_DAY6_APARTMENT};
static const UiStringId apartmentDates[]={UI_DOM_13_DEKABRYA,UI_DOM_14_DEKABRYA,UI_DOM_15_DEKABRYA,UI_DOM_16_DEKABRYA,UI_DOM_17_DEKABRYA,UI_DAY6_DATE};
static const UiStringId ingredients[]={UI_ADELGID,UI_BRONSON_EKSTRAKT,UI_POROSHKOVAYA_DELTA,UI_FLANERGID,UI_KARMOTRIN};
static const UiStringId chatReactions[]={UI_EMPTY,UI_APLODISM,UI_DA_A_A,UI_BU_U,UI_NET,UI_HA_HA,UI_O_O};
static int day_index(int day){return day>=1 && day<=6?day-1:0;}
const char *ui_day_badge(int day){return uiStrings[dayBadges[day_index(day)]];}
const char *ui_day_completed(int day){return uiStrings[dayCompleted[day_index(day)]];}
const char *ui_next_day_hint(int day){return uiStrings[nextDayHints[day>=1 && day<=6?day-1:5]];}
const char *ui_bar_heading(int day,int tutorial){return tutorial?uiStrings[UI_BAR_OBUCHENIE]:uiStrings[barHeadings[day_index(day)]];}
const char *ui_apartment_heading(int day){return uiStrings[apartmentHeadings[day_index(day)]];}
const char *ui_apartment_date(int day){return uiStrings[apartmentDates[day_index(day)]];}
const char *ui_ingredient_name(int ingredient){return uiStrings[ingredients[ingredient>=0 && ingredient<5?ingredient:0]];}
const char *ui_chat_reaction(int reaction){return uiStrings[chatReactions[reaction>=0 && reaction<7?reaction:0]];}

const char *ui_order_hint(int n) {
    switch(n) {
    case 1:return "Сахарный прилив";case 2:return "Взрыв на Луне";
    case 3:case 4:return "Большое пиво";case 5:case 7:return "Пиво";
    case 6:return "Большой горький, без алкоголя";
    case 8:return "Большой Удар по печени";
    case 9:return "Сваебой (или Суплекс)";
    case 10:return "Бон Развязон";
    case 11:return "Маленький сладкий со льдом";
    case 12:return "Изысканный напиток (classy)";
    case 13:case 16:return "Брендини";
    case 14:return "Что-нибудь успокаивающее";
    case 15:return "Пианист / Пианистка";
    case 17:return "Как обычно: пиво";
    case 18:case 23:return "Взрыв на Марсе (Marsblast)";
    case 19:case 26:return "Что-нибудь горькое";
    case 20:return "Пианистка";
    case 21:return "Взрыв на Луне";
    case 22:return "Большой Sunshine Cloud + Gut Punch";
    case 24:return "Похожий на чай: горький, женственный";
    case 25:return "Что-нибудь мягкое";
    case 27:return "Bad Touch";
    case 28:return "Необычный напиток (Promo)";
    case 29:return "Большой Брендини";
    case 30:return "Как обычно: пиво";
    case 31:return "Bleeding Jane";
    case 32:return "Напиток с изменённым названием";
    case 33:return "В честь хорошего друга";
    case 34:return "Два Бон Развязона";
    case 35:return "Две Blue Fairy";
    case 36:return "Напиток за $80";
    case 37:return "Grizzly Temple";
    case 38:return "Мерзкий: Manly или Promo";
    case 39:return "Большой Bad Touch";
    case 40:return "Что-нибудь, чтобы опьянеть";
    case 41:return "Два пива";
    case 42:return "Zen Star";
    case 43:return "Два Брендини";
    case 44:return "Два мужественных (Manly)";
    case 45:return "Взрыв на Марсе";
    case 46:return "Пиво";
    case 47:return "Ром";case 48:return "Blue Fairy";case 49:return "Пиво";
    case 50:return "Cobalt Velvet";case 51:return "Бон Развязон";case 52:return "Абсент";
    case 53:return "Что-нибудь с алкоголем";case 54:return "Брендини";
    case 55:return "Сладкий без алкоголя";case 56:return "Ровно 17 частей ингредиентов";case 57:return "Plumfume";
    case 174:return "Пиво или другой алкоголь";
    default:return "Заказ посетителя";
    }
}
