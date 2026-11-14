# -*- coding: utf-8 -*-
# 世界一周編 ナイロビ+賢者+券選び。会話は創作(5往復)。値段は架空。個人名なし。実在名: Java House / Artcaffe / Safaricom / Pride Lounge / Jomo Kenyatta Intl / Villa Rosa Kempinski / Turkish Airlines / Qatar Airways
D=[]
def d(id,who,bg,sp,intro,pairs,words,**kw):
    D.append(dict(id=id,who=who,bg=bg,sp=sp,intro=intro,pairs=pairs,words=words,**kw))

# ---- 達人賢者 ----
d('sage_1','達人賢者','sage','sage','星の見える広間。達人賢者が、旅のはじまりを教えてくれる。',[
("Welcome, travelers. You want to go around the world?","ようこそ、旅人たち。世界一周をしたいのですか。","*Yes*! *We* *want* to *see* *many* *airports*.","はい。たくさんの空港を見たいです。"),
("Good. One ticket can take you to many countries.","よい。1枚の航空券で、たくさんの国へ行けます。","*Really*? *How* *does* it *work*?","本当ですか。どうやって使うのですか。"),
("You choose a group of airlines. Then you fly from city to city, always going the same way around the earth.","航空会社のグループを選びます。そして、地球をいつも同じ向きに回りながら、都市から都市へ飛びます。","*I* *see*. *Where* *do* we *start*?","なるほど。どこから始めますか。"),
("Your first stop is Nairobi, in Kenya. It is a good place to practice.","最初の寄港地はケニアのナイロビです。練習にぴったりの場所です。","*Nairobi*! *Is* it *far*?","ナイロビ！遠いですか。"),
("It is a long flight. But do not worry. Speak slowly, and smile.","長い飛行です。でも心配はいりません。ゆっくり話して、笑顔でいなさい。","*Thank* you. *We* *will* *try*!","ありがとうございます。がんばります。")],
[("round the world","世界一周"),("ticket","航空券"),("airline","航空会社"),("practice","練習する"),("slowly","ゆっくり")])
d('sage_2','達人賢者','sage','sage','達人賢者に、航空券のえらび方をきいてみよう。',[
("Do you know the two big groups of airlines?","航空会社の大きなグループを2つ知っていますか。","*No*, *I* *don't*. *Please* *tell* me.","いいえ。教えてください。"),
("They are Star Alliance and oneworld. Each group has many airlines.","スターアライアンスとワンワールドです。どちらもたくさんの航空会社があります。","*What's* the *difference*?","何がちがうのですか。"),
("The airlines are different, so the routes are different. But both can take you to every airport on your list.","航空会社がちがうので、ルートもちがいます。でも、どちらでも、あなたの行きたい空港すべてに行けます。","*Can* I *change* my *mind* *later*?","あとで気が変わってもいいですか。"),
("Choose one for this trip. You can choose the other one next time.","この旅ではひとつ選びます。もうひとつは、次の機会に選べます。","*Which* *one* *is* *better*?","どちらがいいですか。"),
("Neither is better. Pick the one that feels fun. A trip should be fun!","どちらがよいということはありません。楽しそうな方を選びなさい。旅は楽しくなくては。","*Okay*. *I'll* *choose* *now*!","わかりました。いま選びます。")],
[("alliance","航空会社の連合"),("route","ルート"),("difference","ちがい"),("change my mind","気が変わる"),("choose","選ぶ")])
d('sage_3','達人賢者','sage','sage','達人賢者から、旅の英語のコツをきこう。',[
("Here is a secret about travel English. Short is good.","旅の英語のひみつを教えましょう。短くて大丈夫です。","*Short* *is* *good*? *Really*?","短くていいのですか。本当に？"),
("Yes. Say 'Excuse me,' then say what you need. People will help you.","はい。『すみません』と言ってから、必要なことを言う。人は助けてくれます。","*What* *if* I *don't* *understand*?","わからなかったらどうしますか。"),
("Say, 'Could you say that again, please?' It is very polite.","『もう一度言っていただけますか』と言いなさい。とても丁寧です。","*Could* *you* *say* *that* *again*, *please*?","もう一度言っていただけますか。"),
("Perfect! And if it is too fast, say, 'Slowly, please.'","完璧です。それでも速すぎたら、『ゆっくりお願いします』と。","*Slowly*, *please*. *I* *can* *do* *that*.","ゆっくりお願いします。できそうです。"),
("You are ready. Now, go and choose your ticket.","準備はできました。さあ、航空券を選びに行きなさい。","*Thank* *you*, *wise* *teacher*!","ありがとうございます、賢者さま。")],
[("excuse me","すみません"),("polite","丁寧な"),("again","もう一度"),("understand","理解する"),("ready","準備ができた")])

# ---- 券選び(2種類) ----
d('ticket_star','スターアライアンスの窓口係','tdesk','desk_star','スターアライアンスの窓口。ターキッシュ エアラインズで、最初の都市ナイロビへ。',[
("Welcome to the Star Alliance desk. Where are you going?","スターアライアンスの窓口へようこそ。どちらへ行かれますか。","*We* *are* *going* *around* the *world*. *First*, *Nairobi*.","世界一周です。まず、ナイロビへ。"),
("Nairobi. Very nice. May I see your passport, please?","ナイロビですね。すてきです。パスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Would you like a window seat or an aisle seat?","ありがとうございます。窓側と通路側、どちらがよいですか。","*A* *window* *seat*, *please*. *I* *want* *to* *see* *the* *clouds*.","窓側をお願いします。雲を見たいので。"),
("A window seat. Do you have any bags to check in?","窓側ですね。預ける荷物はありますか。","*Yes*, *one* *suitcase*.","はい、スーツケースがひとつです。"),
("Here is your boarding pass. Have a wonderful trip!","搭乗券です。すばらしい旅を。","*Thank* *you*! *See* *you* *in* *Nairobi*!","ありがとうございます。ナイロビでお会いしましょう。")],
[("passport","パスポート"),("window seat","窓側の席"),("aisle seat","通路側の席"),("check in","預ける・手続きする"),("boarding pass","搭乗券")])
d('ticket_ow','ワンワールドの窓口係','tdesk','desk_ow','ワンワールドの窓口。カタール航空で、最初の都市ナイロビへ。',[
("Welcome to the oneworld desk. Where are you going?","ワンワールドの窓口へようこそ。どちらへ行かれますか。","*We* *are* *going* *around* the *world*. *First*, *Nairobi*.","世界一周です。まず、ナイロビへ。"),
("Nairobi. Very nice. May I see your passport, please?","ナイロビですね。すてきです。パスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Would you like a window seat or an aisle seat?","ありがとうございます。窓側と通路側、どちらがよいですか。","*An* *aisle* *seat*, *please*. *I* *like* *to* *walk* *around*.","通路側をお願いします。歩き回るのが好きなので。"),
("An aisle seat. Do you have any bags to check in?","通路側ですね。預ける荷物はありますか。","*Yes*, *one* *suitcase*.","はい、スーツケースがひとつです。"),
("Here is your boarding pass. Have a wonderful trip!","搭乗券です。すばらしい旅を。","*Thank* *you*! *See* *you* *in* *Nairobi*!","ありがとうございます。ナイロビでお会いしましょう。")],
[("passport","パスポート"),("aisle seat","通路側の席"),("window seat","窓側の席"),("suitcase","スーツケース"),("boarding pass","搭乗券")])

# ---- 到着: ナイロビ ----
d('nbo_immig1','入国審査の係官','immig','officer','ナイロビのジョモ・ケニヤッタ国際空港に到着。入国審査の列にならんだ。',[
("Good morning. Passport, please.","おはようございます。パスポートをお願いします。","*Good* *morning*. *Here* *you* *are*.","おはようございます。どうぞ。"),
("Do you have your eTA for Kenya?","ケニアのeTA（電子渡航認証）はありますか。","*Yes*. *I* *have* *it* *on* *my* *phone*.","はい。スマホに入っています。"),
("Good. Please look at the camera.","結構です。カメラを見てください。","*Like* *this*?","こうですか。"),
("Yes, that is fine. Now, put your finger here.","はい、それでけっこうです。では、ここに指を置いてください。","*Okay*. *Is* *this* *right*?","はい。これでいいですか。"),
("All done. Welcome to Kenya!","終わりです。ケニアへようこそ。","*Thank* *you*! *Asante*!","ありがとう！アサンテ！")],
[("eTA","電子渡航認証"),("passport","パスポート"),("camera","カメラ"),("finger","指"),("welcome","ようこそ")])
d('nbo_immig2','入国審査の係官','immig','officer2','別の窓口。係官は笑顔で、ゆっくり話してくれる。',[
("Hello. What is the purpose of your visit?","こんにちは。訪問の目的は何ですか。","*I'm* *a* *tourist*. *I'm* *on* *a* *trip* *around* *the* *world*.","観光です。世界一周の旅の途中です。"),
("Wonderful! How long will you stay in Kenya?","すばらしい。ケニアにはどのくらい滞在しますか。","*For* *three* *days*.","3日間です。"),
("Where will you stay in Nairobi?","ナイロビではどこに泊まりますか。","*At* *the* *Villa* *Rosa* *Kempinski*.","ヴィラ・ローザ・ケンピンスキーです。"),
("Do you have a ticket to leave Kenya?","ケニアを出る航空券はありますか。","*Yes*. *I* *fly* *out* *in* *three* *days*.","はい。3日後に出発します。"),
("Good. Enjoy your stay. Karibu Kenya!","結構です。滞在を楽しんで。ようこそケニアへ！","*Thank* *you*. *I* *will*!","ありがとうございます。楽しみます。")],
[("purpose","目的"),("tourist","観光客"),("stay","滞在する"),("hotel","ホテル"),("leave","出発する")])
d('nbo_bag1','手荷物受け取りのスタッフ','baggage','bag_staff','手荷物受け取り。ベルトコンベアから、スーツケースが出てこない。',[
("Hello. Can I help you?","こんにちは。お手伝いしましょうか。","*Yes*. *My* *suitcase* *is* *not* *here*.","はい。スーツケースが見つかりません。"),
("I am sorry. What color is your suitcase?","申し訳ありません。スーツケースは何色ですか。","*It's* *blue*, *with* *a* *yellow* *tag*.","青で、黄色いタグがついています。"),
("May I see your baggage tag, please?","荷物のタグを見せていただけますか。","*Here* *it* *is*.","これです。"),
("Thank you. Please wait here. I will check the system.","ありがとうございます。ここでお待ちください。システムを確認します。","*How* *long* *will* *it* *take*?","どのくらいかかりますか。"),
("It is here! It came on the next belt. Enjoy Nairobi!","ありました！次のベルトで来ていました。ナイロビを楽しんで。","*Oh*, *thank* *goodness*! *Thank* *you*!","よかった！ありがとうございます。")],
[("suitcase","スーツケース"),("tag","タグ"),("belt","ベルトコンベア"),("check","確認する"),("sorry","申し訳ない")])
d('nbo_bag2','手荷物受け取りのスタッフ','baggage','bag_staff2','スーツケースを受け取ったところで、係の人に声をかけられた。',[
("Welcome to Kenya. Do you have any plastic bags in your suitcase?","ケニアへようこそ。スーツケースにレジ袋は入っていますか。","*Plastic* *bags*? *Why*?","レジ袋ですか。なぜですか。"),
("In Kenya, single-use plastic bags are not allowed. We use paper or cloth bags.","ケニアでは、使い捨てのレジ袋は禁止されています。紙か布の袋を使います。","*I* *see*. *I* *have* *a* *cloth* *bag*.","なるほど。布の袋ならあります。"),
("That is perfect. Please keep using it during your trip.","それは完璧です。旅の間、それを使ってください。","*Of* *course*. *Is* *the* *airport* *clean*?","もちろんです。空港はきれいですか。"),
("Yes, we try to keep Kenya clean and green.","はい、ケニアをきれいで緑豊かに保つようにしています。","*That's* *wonderful*.","すばらしいですね。"),
("Thank you for helping. Enjoy your trip!","協力ありがとうございます。旅を楽しんで。","*Thank* *you*. *Have* *a* *nice* *day*!","ありがとうございます。よい一日を。")],
[("plastic bag","レジ袋"),("allowed","許可されている"),("cloth","布"),("clean","きれいな"),("keep","保つ")])
d('nbo_sim1','Safaricomの店員','sim','sim_staff','到着ロビーの Safaricom の店。現地のSIMカードを買おう。',[
("Jambo! Welcome to Safaricom. How can I help?","ジャンボ！Safaricomへようこそ。ご用件は何ですか。","*I* *need* *a* *SIM* *card*, *please*.","SIMカードがほしいです。"),
("Sure. May I see your passport? We must register your SIM.","かしこまりました。パスポートを見せてください。SIMの登録が必要です。","*Here* *is* *my* *passport*.","パスポートです。"),
("Thank you. Do you want data for seven days?","ありがとうございます。7日間のデータはいかがですか。","*Yes*. *How* *much* *data* *is* *it*?","はい。データ量はどのくらいですか。"),
("Five gigabytes. It costs one thousand shillings.","5ギガバイトです。料金は1000シリングです。","*That's* *fine*. *Can* *I* *pay* *by* *card*?","けっこうです。カードで払えますか。"),
("Yes, you can. Your SIM is ready. Enjoy Kenya!","はい、できます。SIMの準備ができました。ケニアを楽しんで。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("SIM card","SIMカード"),("register","登録する"),("data","データ通信"),("gigabyte","ギガバイト"),("pay by card","カードで払う")])
d('nbo_sim2','Safaricomの店員','sim','sim_staff2','別の店員さん。スマホの設定がうまくいかないようだ。',[
("Hello. Is your phone working?","こんにちは。スマホは動いていますか。","*No*. *I* *can't* *use* *the* *internet*.","いいえ。インターネットが使えません。"),
("Let me see. Please turn your phone off and on again.","見てみましょう。スマホの電源を切って、また入れてください。","*Okay*. *Wait* *a* *moment*.","わかりました。少し待ってください。"),
("Do you see the signal bars now?","電波のバーが見えますか。","*Yes*! *I* *see* *four* *bars*.","はい！4本立っています。"),
("Good. Now open your browser and try a website.","よかった。ブラウザを開いて、サイトを見てみてください。","*It* *works*! *Thank* *you* *so* *much*.","つながりました！ありがとうございます。"),
("You are welcome. You can also use M-Pesa for payments here.","どういたしまして。ここではM-Pesaでの支払いも使えますよ。","*Great*. *I'll* *remember* *that*.","いいですね。覚えておきます。")],
[("internet","インターネット"),("turn off","電源を切る"),("signal","電波"),("browser","ブラウザ"),("payment","支払い")])
d('nbo_taxi1','タクシー乗り場の係員','taxi','taxi_staff','空港の外。ホテルまでどうやって行こう。',[
("Hello, my friend. Do you need a taxi?","こんにちは。タクシーが必要ですか。","*Yes*. *Please*. *To* *the* *Villa* *Rosa* *Kempinski*.","はい、お願いします。ヴィラ・ローザ・ケンピンスキーまで。"),
("Sure. Please wait in this line. The next car is yours.","かしこまりました。この列でお待ちください。次の車があなたたちのです。","*How* *much* *is* *it*, *please*?","料金はいくらですか。"),
("It is a fixed price. Three thousand shillings to the city.","定額です。市内まで3000シリングです。","*Okay*. *How* *long* *does* *it* *take*?","わかりました。どのくらいかかりますか。"),
("About forty minutes. The traffic is busy in the morning.","約40分です。朝は道がこみます。","*That's* *fine*. *We're* *not* *in* *a* *hurry*.","けっこうです。急いでいません。"),
("Good. Here is your car. Please watch your step.","よかった。こちらがお車です。足元にご注意ください。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("taxi","タクシー"),("fixed price","定額"),("traffic","交通量"),("busy","混んでいる"),("in a hurry","急いでいる")])
d('nbo_taxi2','ライドシェアの運転手','taxi','driver','Uber アプリで車を呼んだ。待ち合わせ場所に、車がやって来た。',[
("Hello! Are you the passengers for the hotel?","こんにちは！ホテルへ行くお客さんですか。","*Yes*, *that's* *us*. *Is* *this* *the* *Uber*?","はい、私たちです。Uberですか。"),
("Yes. May I have the last four numbers of your phone?","はい。電話番号の下4けたを教えてください。","*Sure*. *It's* *one*, *two*, *three*, *four*.","もちろん。1、2、3、4です。"),
("Perfect. Let me help with your suitcase.","ばっちりです。スーツケースをお持ちします。","*Thank* *you*. *It's* *a* *little* *heavy*.","ありがとう。少し重いんです。"),
("No problem. Do you want the air conditioner on?","問題ありません。エアコンはつけますか。","*Yes*, *please*. *A* *little* *cool*.","はい、お願いします。少し涼しく。"),
("Good. Sit back and enjoy the ride!","よし。ゆったり座って、ドライブを楽しんで。","*Thank* *you*. *Let's* *go*!","ありがとう。行きましょう！")],
[("passenger","乗客"),("suitcase","スーツケース"),("heavy","重い"),("air conditioner","エアコン"),("ride","乗ること")])

# ---- 空港: ナイロビ ----
d('nbo_java1','Java Houseの店員','cafeK','cafe_staff','Java House に入った。コーヒーのいい香り。',[
("Jambo! Welcome to Java House. What can I get you?","ジャンボ！Java Houseへようこそ。ご注文は？","*I'd* *like* *a* *latte*, *please*.","ラテをお願いします。"),
("Sure. Hot or iced?","かしこまりました。ホットですか、アイスですか。","*Hot*, *please*. *And* *a* *slice* *of* *cake*.","ホットでお願いします。それとケーキをひと切れ。"),
("We have chocolate and carrot cake. Which one?","チョコレートとキャロットのケーキがあります。どちらにしますか。","*Carrot* *cake*, *please*.","キャロットケーキをお願いします。"),
("Okay. That is eight hundred shillings.","はい。800シリングです。","*Can* *I* *pay* *by* *card*?","カードで払えますか。"),
("Yes. Here you go. Enjoy!","はい。どうぞ。ごゆっくり。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("latte","ラテ"),("iced","冷たい・氷入りの"),("slice","ひと切れ"),("carrot cake","キャロットケーキ"),("shillings","シリング(ケニアのお金)")])
d('nbo_java2','Java Houseの店員','cafeK','cafe_staff2','店は混んでいる。隣のお客さんが話しかけてきた。',[
("Excuse me. Is this seat free?","すみません。この席は空いていますか。","*Yes*, *it* *is*. *Please* *sit* *down*.","はい、空いています。どうぞ座ってください。"),
("Thank you. Are you traveling?","ありがとう。旅行中ですか。","*Yes*. *We* *are* *traveling* *around* *the* *world*.","はい。世界一周をしています。"),
("Wow! How do you like Nairobi so far?","わあ！ナイロビはここまでどうですか。","*It's* *great*. *The* *people* *are* *very* *kind*.","すばらしいです。人々がとても親切で。"),
("Thank you. You must try nyama choma before you leave.","ありがとう。帰る前にニャマチョマ（焼き肉）を食べてみて。","*Nyama* *choma*? *What* *is* *that*?","ニャマチョマ？それは何ですか。"),
("Grilled meat! It is our favorite. Enjoy your trip!","焼いたお肉です！みんな大好きなんですよ。旅を楽しんで！","*I* *will*. *Thank* *you* *for* *the* *tip*!","そうします。教えてくれてありがとう！")],
[("seat","席"),("traveling","旅行している"),("kind","親切な"),("grilled","焼いた"),("tip","アドバイス・コツ")])
d('nbo_art1','Artcaffeの店員','cafeK','cafe_staff3','Artcaffe に入った。パンのやけるにおいがする。',[
("Hello! Welcome to Artcaffe. Eat in or take away?","こんにちは！Artcaffeへようこそ。店内ですか、お持ち帰りですか。","*Eat* *in*, *please*.","店内でお願いします。"),
("Okay. Here is the menu. Would you like some water?","はい。こちらがメニューです。お水はいかがですか。","*Yes*, *please*. *What* *do* *you* *recommend*?","はい、お願いします。おすすめは何ですか。"),
("Our fresh bread and passion juice are popular.","焼きたてパンとパッションジュースが人気です。","*I'll* *have* *the* *passion* *juice*, *and* *bread*.","パッションジュースとパンをください。"),
("Good choice. Anything else?","いい選択です。ほかには？","*That's* *all*, *thank* *you*.","以上です、ありがとう。"),
("Coming right up! Please sit anywhere.","すぐお持ちします！お好きな席へどうぞ。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("eat in","店内で食べる"),("take away","持ち帰り"),("recommend","おすすめする"),("passion juice","パッションフルーツのジュース"),("popular","人気のある")])
d('nbo_art2','Artcaffeの店員','cafeK','cafe_staff4','お会計のとき、店員さんが話しかけてくれた。',[
("How was everything today?","今日はいかがでしたか。","*It* *was* *delicious*. *The* *bread* *was* *so* *soft*.","とてもおいしかったです。パンがやわらかくて。"),
("I am glad. Where are you from?","うれしいです。どちらから来ましたか。","*We* *are* *from* *Japan*.","日本からです。"),
("Japan! That is far. How long have you been traveling?","日本！遠いですね。旅はどのくらいですか。","*Only* *two* *days*. *This* *is* *our* *first* *stop*.","まだ2日です。ここが最初の寄港地です。"),
("Then you must see the animals. Nairobi National Park is close.","それなら動物を見なくちゃ。ナイロビ国立公園は近いですよ。","*Really*? *We* *would* *love* *to* *go*.","本当ですか。ぜひ行きたいです。"),
("Enjoy your trip! Come again soon.","旅を楽しんで！またいらしてくださいね。","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("delicious","おいしい"),("soft","やわらかい"),("far","遠い"),("national park","国立公園"),("close","近い")])
d('nbo_lounge1','Pride Loungeの受付','lounge','lounge_staff','Pride Lounge に着いた。受付の人がにこやかに迎えてくれる。',[
("Welcome to the Pride Lounge. May I see your boarding pass?","Pride Loungeへようこそ。搭乗券を見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Please enjoy the lounge. Do you need Wi-Fi?","ありがとうございます。どうぞお楽しみください。Wi-Fiは必要ですか。","*Yes*, *please*. *What's* *the* *password*?","はい、お願いします。パスワードは何ですか。"),
("It is on the card. Please connect to the lounge network.","カードに書いてあります。ラウンジのネットワークに接続してください。","*Thank* *you*. *Where* *can* *I* *get* *a* *drink*?","ありがとう。飲み物はどこでもらえますか。"),
("The bar is on the left. There is also food in the middle.","バーは左側です。中央には食事もあります。","*Great*. *Is* *there* *a* *quiet* *area*?","いいですね。静かな場所はありますか。"),
("Yes, at the back. Please relax and enjoy.","はい、奥にあります。ゆっくりくつろいでください。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("lounge","ラウンジ"),("password","パスワード"),("connect","接続する"),("quiet","静かな"),("relax","くつろぐ")])
d('nbo_lounge2','ラウンジの隣の席のお客さん','lounge','lounge_guest','ラウンジのソファ。隣のお客さんが笑顔であいさつしてくれた。',[
("Hello! Is this your first time in Kenya?","こんにちは！ケニアは初めてですか。","*Yes*, *it* *is*. *We* *just* *arrived*.","はい。着いたばかりです。"),
("Welcome! What are you going to do here?","ようこそ！ここで何をする予定ですか。","*We* *want* *to* *see* *the* *giraffes*.","キリンを見たいです。"),
("There is a giraffe center near Nairobi. You can feed them!","ナイロビの近くにキリンセンターがあります。えさをあげられますよ！","*That* *sounds* *fun*! *Is* *it* *safe*?","楽しそう！安全ですか。"),
("Yes. The giraffes are gentle. They love the snacks.","はい。キリンはおだやかです。おやつが大好きなんですよ。","*I* *can't* *wait*. *Thank* *you*!","待ちきれません。ありがとう！"),
("Enjoy! Safari njema! That means good journey.","楽しんで！サファリ・ンジェマ！「よい旅を」という意味です。","*Safari* *njema*! *Thank* *you*!","サファリ・ンジェマ！ありがとう！")],
[("giraffe","キリン"),("feed","えさをあげる"),("safe","安全な"),("gentle","おだやかな"),("journey","旅")])
d('nbo_duty1','免税店の店員','duty','duty_staff','免税店で、ケニアのコーヒーを見つけた。',[
("Welcome! Are you looking for something special?","いらっしゃいませ！何かお探しですか。","*Yes*. *I* *want* *Kenyan* *coffee* *for* *my* *family*.","はい。家族にケニアのコーヒーをおみやげにしたいです。"),
("Good choice. This one is from the mountains. It is very smooth.","いい選択です。これは山で育ったコーヒーです。とてもまろやかですよ。","*How* *much* *is* *it*?","いくらですか。"),
("It is twelve dollars for one bag.","1袋12ドルです。","*I'll* *take* *two* *bags*, *please*.","2袋ください。"),
("Two bags. Would you like a gift box?","2袋ですね。ギフトボックスはどうしますか。","*Yes*, *please*. *It's* *a* *present*.","はい、お願いします。プレゼントなので。"),
("Done! Here is your receipt. Thank you!","できました！レシートです。ありがとうございます！","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("coffee","コーヒー"),("smooth","まろやか"),("gift box","ギフトボックス"),("present","贈り物"),("receipt","レシート")])
d('nbo_duty2','免税店の店員','duty','duty_staff2','隣の棚には、ケニアの紅茶と、カラフルな布がならんでいる。',[
("Hello! Would you like to try some Kenyan tea?","こんにちは！ケニアの紅茶を試してみませんか。","*Yes*, *please*. *It* *smells* *nice*.","はい、お願いします。いい香りです。"),
("Here you go. Be careful. It is hot.","どうぞ。気をつけて。熱いですよ。","*Mmm*, *it's* *delicious*. *Is* *it* *strong*?","おいしい。濃いですか。"),
("A little strong. Many people add milk and sugar.","少し濃いです。ミルクと砂糖を入れる人が多いですよ。","*I'll* *buy* *a* *box* *of* *tea*.","紅茶を1箱買います。"),
("Great. And this colorful cloth is called kikoi. Do you like it?","いいですね。このカラフルな布は「キコイ」といいます。いかがですか。","*It's* *beautiful*. *I'll* *take* *a* *blue* *one*.","きれいですね。青いのをください。"),
("Lovely. Thank you for shopping with us!","すてきです。お買い上げありがとうございます！","*Thank* *you*. *Have* *a* *good* *day*!","ありがとう。よい一日を！")],
[("tea","紅茶"),("strong","濃い"),("sugar","砂糖"),("colorful","カラフルな"),("beautiful","美しい")])
d('nbo_gate1','搭乗ゲートの係員','gate','gate_agent','搭乗ゲートに着いた。アナウンスが流れている。',[
("Good afternoon. May I see your boarding pass and passport?","こんにちは。搭乗券とパスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Boarding will begin in twenty minutes.","ありがとうございます。搭乗は20分後に始まります。","*Is* *this* *the* *right* *gate*?","ここで合っていますか。"),
("Yes, this is the correct gate. Please wait over there.","はい、このゲートで合っています。あちらでお待ちください。","*Can* *I* *buy* *a* *drink* *first*?","先に飲み物を買ってもいいですか。"),
("Of course. Just come back before boarding.","もちろん。搭乗前に戻ってくればだいじょうぶです。","*Thank* *you*. *I'll* *be* *back* *soon*.","ありがとう。すぐ戻ります。"),
("No problem. Have a safe flight!","問題ありません。よい旅を！","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("gate","搭乗ゲート"),("boarding","搭乗"),("correct","正しい"),("wait","待つ"),("flight","フライト")])
d('nbo_gate2','搭乗ゲートの係員','gate','gate_agent2','ゲートの前に人がたくさん。次の都市へ出発する時間が近づいている。',[
("Attention please. Flight boarding is now open.","お知らせします。搭乗が始まりました。","*Excuse* *me*. *Can* *we* *board* *now*?","すみません。いま乗れますか。"),
("Which group are you in?","何番のグループですか。","*We* *are* *in* *group* *two*.","グループ2です。"),
("Group two will board in a few minutes. Please wait.","グループ2は数分後です。お待ちください。","*Okay*. *Is* *the* *flight* *on* *time*?","わかりました。フライトは定刻ですか。"),
("Yes, on time. You will like the view from the window.","はい、定刻です。窓からの景色を気に入りますよ。","*I* *love* *the* *view*. *I* *can't* *wait*.","景色が大好きです。待ちきれません。"),
("Group two, please come forward now. Enjoy your trip!","グループ2の方、どうぞお進みください。旅を楽しんで！","*Thank* *you*. *Goodbye*, *Nairobi*!","ありがとう。さようなら、ナイロビ！")],
[("attention","お知らせ"),("board","搭乗する"),("on time","定刻の"),("view","景色"),("come forward","前に進む")])

# ---- 出発: ナイロビ(Qatar Airways でドーハへ) ----
# 実在名: Qatar Airways。飛行時間 約5時間(2026-11-14 確認、資料は5時間〜5時間20分)。重さ・時刻・席番号は架空。
d('nbo_checkin1','Qatar Airwaysのチェックイン係','checkinQ','qr_checkin','ナイロビの空港、Qatar Airwaysのカウンター。係の人が明るく手をふっている。',[
("Jambo! Welcome to Qatar Airways. Where are you flying today?","ジャンボ！カタール航空へようこそ。今日はどちらへ？","*Jambo*! *We* *are* *flying* *to* *Doha*.","ジャンボ！ドーハへ行きます。"),
("Lovely. Please put your suitcase on the scale.","いいですね。スーツケースをはかりにのせてください。","*Sure*. *Is* *it* *too* *heavy*?","はい。重すぎますか。"),
("No, it is fine. Is Doha your final stop today?","いいえ、大丈夫です。今日の最終目的地はドーハですか。","*Yes*. *We* *will* *stay* *in* *Doha* *for* *one* *night*.","はい。ドーハに1泊します。"),
("Then your bag goes to Doha. Here is your baggage tag.","では荷物はドーハまでです。こちらが手荷物の引換証です。","*Thank* *you*. *What* *time* *does* *boarding* *start*?","ありがとう。搭乗は何時に始まりますか。"),
("Forty minutes before the flight. Have a good trip!","出発の40分前です。よい旅を！","*Asante*! *Goodbye*, *Nairobi*!","アサンテ！さよなら、ナイロビ！")],
[("scale","はかり"),("heavy","重い"),("final stop","最終目的地"),("baggage tag","手荷物の引換証"),("boarding","搭乗")])
d('nbo_checkin2','Qatar Airwaysのチェックイン係','checkinQ','qr_checkin2','となりのカウンター。係の人が、画面を見て少しこまった顔をしている。',[
("Good evening. Passports, please. Two passengers?","こんばんは。パスポートをお願いします。お二人ですか。","*Yes*, *two*. *Here* *are* *our* *passports*.","はい、二人です。パスポートです。"),
("Thank you. I am sorry, but your seats are not together.","ありがとうございます。すみません、お席がはなれています。","*Oh* *no*. *Can* *we* *sit* *together*, *please*?","そんな。いっしょに座れますか。"),
("Let me check. One moment. I have two seats in row thirty.","お調べします。少々お待ちを。30列目に2席あります。","*Great*! *Is* *one* *of* *them* *a* *window* *seat*?","よかった！どちらかは窓側ですか。"),
("Yes. Thirty A is by the window, and thirty B is next to it.","はい。30Aが窓側で、30Bがそのとなりです。","*Perfect*. *We* *will* *take* *them*.","完ぺきです。その席にします。"),
("All done. Here are your new boarding passes.","できました。新しい搭乗券です。","*Thank* *you* *for* *your* *help*!","助かりました。ありがとう！")],
[("passenger","乗客"),("together","いっしょに"),("one moment","少々お待ちください"),("row","列"),("next to","〜のとなり")])
d('nbo_sec1','保安検査の係員','security','sec_n1','保安検査の列。係員はてきぱきと、でもやさしく声をかけている。',[
("Next, please. Put your bags on the belt.","次の方どうぞ。荷物をベルトにのせてください。","*Okay*. *Do* *I* *take* *out* *my* *laptop*?","はい。ノートパソコンは出しますか。"),
("Yes. Laptops and tablets go in a separate tray.","はい。パソコンとタブレットはべつのトレーに入れます。","*All* *right*. *What* *about* *my* *jacket*?","わかりました。上着はどうしますか。"),
("Jackets off, please. And your belt and watch.","上着はぬいでください。ベルトと時計もお願いします。","*Okay*. *Here* *is* *my* *belt*.","はい。ベルトです。"),
("Do you have any liquids in your bag?","かばんに液体は入っていますか。","*Only* *a* *small* *bottle* *of* *water*.","小さい水のボトルだけです。"),
("Sorry, you cannot take water through. Please empty the bottle.","すみません、水は持ちこめません。ボトルを空にしてください。","*I* *see*. *I* *will* *drink* *it* *now*.","わかりました。今飲みます。")],
[("laptop","ノートパソコン"),("separate","べつの"),("tray","トレー"),("liquids","液体"),("empty","空にする")])
d('nbo_sec2','保安検査の係員','security','sec_n2','検査のあと、かばんが1つだけ横によけられた。係員が手まねきしている。',[
("Excuse me. Is this your bag?","すみません。これはあなたのかばんですか。","*Yes*, *it* *is* *mine*. *Is* *there* *a* *problem*?","はい、私のです。何か問題がありますか。"),
("I need to open it. Is that okay?","中を開けて見ます。よろしいですか。","*Sure*. *Go* *ahead*.","はい。どうぞ。"),
("What is this long thing?","この長いものは何ですか。","*It* *is* *a* *wooden* *giraffe*. *It* *is* *a* *souvenir*.","木のキリンです。おみやげです。"),
("Ah, a giraffe! Very nice. No problem.","ああ、キリンですね。すてきです。問題ありません。","*Thank* *you*. *Can* *I* *close* *my* *bag*?","ありがとう。かばんを閉めてもいいですか。"),
("Yes. You are good to go. Have a safe flight.","はい。行って大丈夫です。安全な空の旅を。","*Thanks*. *Have* *a* *nice* *day*!","ありがとう。よい一日を！")],
[("problem","問題"),("go ahead","どうぞ"),("wooden","木の"),("souvenir","おみやげ"),("safe flight","安全な空の旅")])
d('nbo_plane1','Qatar Airwaysの客室乗務員','cabinQ','qr_crew','ついに機内へ。客室乗務員が、おだやかな声でむかえてくれた。',[
("Good evening. Welcome aboard. May I see your boarding pass?","こんばんは。ご搭乗ありがとうございます。搭乗券を見せていただけますか。","*Good* *evening*. *Here* *it* *is*.","こんばんは。これです。"),
("Thirty A. Go down this aisle. It is on your left.","30Aですね。この通路を進んでください。左側です。","*Thank* *you*. *Is* *there* *space* *for* *my* *bag*?","ありがとう。かばんを入れる場所はありますか。"),
("Yes, in the overhead bin. Let me help you.","はい、頭上の荷物入れに。お手伝いします。","*That* *is* *very* *kind*. *Thank* *you*.","ご親切にどうも。ありがとう。"),
("My pleasure. Would you like water or juice before takeoff?","どういたしまして。離陸の前に、水かジュースはいかがですか。","*Water*, *please*. *And* *may* *I* *have* *a* *blanket*?","水をお願いします。毛布もいただけますか。"),
("Of course. The flight to Doha takes about five hours.","もちろんです。ドーハまでは約5時間です。","*Great*. *Goodbye*, *Nairobi*!","いいですね。さよなら、ナイロビ！")],
[("aboard","搭乗して"),("aisle","通路"),("overhead bin","頭上の荷物入れ"),("takeoff","離陸"),("blanket","毛布")])
d('nbo_plane2','Qatar Airwaysの客室乗務員','cabinQ','qr_crew2','雲の上。食事のカートが、しずかに近づいてきた。',[
("Excuse me. Chicken with rice, or vegetable pasta?","失礼します。チキンとライス、または野菜のパスタ、どちらになさいますか。","*Sorry*, *could* *you* *say* *that* *again*?","すみません、もう一度言ってもらえますか。"),
("Of course. Chicken with rice, or vegetable pasta?","もちろんです。チキンとライス、または野菜のパスタです。","*Chicken* *with* *rice*, *please*.","チキンとライスをお願いします。"),
("Certainly. And something to drink?","かしこまりました。お飲み物はいかがですか。","*Do* *you* *have* *hot* *tea*?","温かい紅茶はありますか。"),
("Yes, we do. With milk and sugar?","はい、ございます。ミルクと砂糖は入れますか。","*Just* *milk*, *please*.","ミルクだけお願いします。"),
("Here you are. We will land in Doha in two hours.","どうぞ。あと2時間でドーハに着陸します。","*Thank* *you*. *I* *can't* *wait*!","ありがとう。待ちきれません！")],
[("say that again","もう一度言う"),("vegetable","野菜"),("something to drink","飲み物"),("sugar","砂糖"),("land","着陸する")])

# ---- 到着: ドーハ(ハマド国際空港) ----
# 実在名: Hamad International Airport / Ooredoo(到着ロビーの売店) / Karwa(メーター制のタクシー) / Doha Metro Red Line / Msheireb(乗りかえ駅) / Souq Waqif
# 2026-11-14 確認。値段・ベルト番号は架空。話し方は、ていねいで落ち着いた調子(ナイロビの明るさと変える)。
d('doh_immig1','入国審査の係官','dimmig','d_officer','ドーハのハマド国際空港に到着。広くてしずかな入国審査。係官は、短くていねいに話す。',[
("Good evening. Passport, please.","こんばんは。パスポートをお願いします。","*Good* *evening*. *Here* *you* *are*.","こんばんは。どうぞ。"),
("How long will you stay in Qatar?","カタールにはどのくらい滞在しますか。","*Only* *one* *night*. *We* *fly* *to* *Helsinki* *tomorrow*.","1泊だけです。明日ヘルシンキへ飛びます。"),
("Do you have your onward ticket?","次の行き先への航空券はありますか。","*Yes*. *It* *is* *on* *my* *phone*. *Here*.","はい。スマホに入っています。これです。"),
("Thank you. Please look at the camera, and do not smile.","ありがとうございます。カメラを見てください。笑わないでくださいね。","*Okay*. *Like* *this*?","はい。こうですか。"),
("Yes. You may go. Enjoy your stay in Qatar.","はい。お進みください。カタールでの滞在を楽しんで。","*Thank* *you* *very* *much*.","どうもありがとうございます。")],
[("stay","滞在する"),("tomorrow","明日"),("onward ticket","次の行き先への航空券"),("smile","ほほえむ"),("enjoy","楽しむ")])
d('doh_immig2','入国審査の係官','dimmig','d_officer2','別の窓口。ホテルの名前を聞かれて、頭がまっ白になった。',[
("Next, please. Where will you stay tonight?","次の方どうぞ。今夜はどこに泊まりますか。","*At* *a* *hotel* *near* *Souq* *Waqif*.","スーク・ワキーフの近くのホテルです。"),
("What is the name of the hotel?","ホテルの名前は何ですか。","*Sorry*, *I* *forgot* *the* *name*. *One* *moment*, *please*.","すみません、名前を忘れました。少し待ってください。"),
("Take your time. Do you have the booking?","ごゆっくりどうぞ。予約はありますか。","*Yes*! *Here* *is* *the* *booking* *on* *my* *phone*.","はい！スマホに予約があります。"),
("I see it. Thank you. What is the purpose of your visit?","確認しました。ありがとうございます。訪問の目的は何ですか。","*Sightseeing*. *We* *want* *to* *see* *the* *old* *market*.","観光です。古い市場を見たいです。"),
("Very good. Welcome to Qatar.","けっこうです。カタールへようこそ。","*Thank* *you*. *Have* *a* *good* *night*.","ありがとう。おやすみなさい。")],
[("tonight","今夜"),("forgot","忘れた"),("booking","予約"),("sightseeing","観光"),("market","市場")])
d('doh_bag1','手荷物受け取りのスタッフ','dbag','d_bag','手荷物受け取り。制服のスタッフが、すぐに気づいて声をかけてくれた。',[
("Good evening, sir. May I help you?","こんばんは。お手伝いしましょうか。","*Yes*, *please*. *Where* *is* *the* *bag* *from* *Nairobi*?","お願いします。ナイロビからの荷物はどこですか。"),
("The flight from Nairobi is on belt number eight.","ナイロビからの便は8番のベルトです。","*Belt* *eight*. *Is* *it* *far* *from* *here*?","8番ですね。ここから遠いですか。"),
("No, it is just over there, on your right.","いいえ、すぐあそこ、右側です。","*Thank* *you*. *May* *I* *use* *this* *trolley*?","ありがとう。このカートを使ってもいいですか。"),
("Yes, of course. Please take one.","はい、もちろんです。お使いください。","*Great*. *How* *long* *will* *the* *bags* *take*?","よかった。荷物はどのくらいで出てきますか。"),
("About ten minutes. Thank you for waiting.","10分ほどです。お待ちいただきありがとうございます。","*No* *problem*. *Thank* *you*!","大丈夫です。ありがとう！")],
[("belt","ベルト(荷物のレーン)"),("far","遠い"),("over there","あそこ"),("trolley","カート"),("waiting","待つこと")])
d('doh_bag2','となりの旅行者','dbag','d_traveler','ベルトの前。同じ黒いスーツケースに、となりの人も手をのばした。',[
("Excuse me, I think this black suitcase is mine.","すみません、この黒いスーツケースは私のだと思います。","*Sorry*, *but* *I* *think* *it* *is* *ours*. *Look* *at* *the* *name* *tag*.","すみません、私たちのだと思います。名札を見てください。"),
("Oh! You are right. It is not my name. I am so sorry.","あっ！そのとおりです。私の名前ではありません。本当にごめんなさい。","*That's* *okay*. *They* *look* *the* *same*.","大丈夫です。そっくりですから。"),
("Mine has a red ribbon on the handle.","私のは、持ち手に赤いリボンがついています。","*A* *red* *ribbon*? *I* *see* *one* *over* *there*!","赤いリボン？あそこに1つ見えます！"),
("Yes, that is mine! Thank you so much.","そう、あれが私のです！本当にありがとう。","*You're* *welcome*. *Where* *are* *you* *from*?","どういたしまして。どちらからですか。"),
("I am from India. I work here in Doha. Welcome!","インドからです。ここドーハで働いています。ようこそ！","*Thank* *you*! *Have* *a* *good* *night*.","ありがとう！おやすみなさい。")],
[("mine","私のもの"),("name tag","名札"),("the same","同じ"),("ribbon","リボン"),("handle","持ち手")])
d('doh_sim1','Ooredooの店員','dsim','d_sim','到着ロビーのOoredoo。店員は手ぎわがよく、話もはやい。',[
("Welcome to Ooredoo. How can I help you today?","Ooredooへようこそ。ご用件は何でしょうか。","*Hello*. *I* *need* *a* *SIM* *card* *for* *one* *day*.","こんにちは。1日だけ使うSIMカードがほしいです。"),
("We have a visitor SIM. It is good for seven days.","旅行者用のSIMがあります。7日間使えます。","*Seven* *days* *is* *fine*. *How* *much* *is* *it*?","7日間でいいです。いくらですか。"),
("It is thirty riyals. May I have your passport?","30リヤルです。パスポートをお借りできますか。","*Here* *you* *are*. *Can* *I* *pay* *by* *card*?","どうぞ。カードで払えますか。"),
("Yes, card is fine. I will set it up for you.","はい、カードで大丈夫です。こちらで設定します。","*Thank* *you*. *Does* *it* *work* *now*?","ありがとう。もう使えますか。"),
("Yes, it is ready. Enjoy your stay in Doha.","はい、準備できました。ドーハでの滞在を楽しんで。","*That* *was* *fast*! *Thank* *you*.","はやい！ありがとう。")],
[("visitor","訪問者"),("riyal","リヤル(カタールのお金)"),("pay by card","カードで払う"),("set up","設定する"),("ready","準備ができた")])
d('doh_sim2','Ooredooの店員','dsim','d_sim2','SIMを入れたのに、地図が開かない。もう一度カウンターへ。',[
("Hello again. Is everything all right?","またいらっしゃいましたね。何かありましたか。","*No*. *The* *internet* *does* *not* *work*.","いいえ。インターネットがつながりません。"),
("Let me see. May I have your phone?","見てみましょう。スマホをお借りできますか。","*Sure*. *Here* *it* *is*.","はい。どうぞ。"),
("Ah. Mobile data is off. I will turn it on.","ああ。モバイルデータがオフです。オンにしますね。","*Oh*, *I* *see*. *Is* *it* *working* *now*?","そうだったんですね。もう動いていますか。"),
("Yes. Please open a map and try.","はい。地図を開いて試してください。","*It* *works*! *I* *can* *see* *the* *map*.","つながった！地図が見えます。"),
("Good. If you have any trouble, please come back.","よかったです。こまったら、またいらしてください。","*I* *will*. *Thank* *you* *for* *your* *help*.","そうします。助かりました。")],
[("internet","インターネット"),("mobile data","モバイルデータ通信"),("turn on","オンにする"),("try","試す"),("trouble","こまったこと")])
d('doh_taxi','Karwaタクシーの係員','dtaxi','d_taxi','到着ロビーのはしにあるタクシー乗り場。係員が、しずかに手で列を案内している。',[
("Good evening. Taxi? This way, please.","こんばんは。タクシーですか。こちらへどうぞ。","*Yes*, *please*. *We* *are* *going* *to* *Souq* *Waqif*.","お願いします。スーク・ワキーフへ行きます。"),
("Souq Waqif. It takes about twenty minutes.","スーク・ワキーフですね。20分ほどです。","*Good*. *Does* *the* *taxi* *use* *a* *meter*?","よかった。タクシーはメーターを使いますか。"),
("Yes, all Karwa taxis use a meter.","はい、Karwaのタクシーはすべてメーター制です。","*Can* *I* *pay* *by* *card*?","カードで払えますか。"),
("Yes, card or cash. Please take the next taxi in line.","はい、カードでも現金でも。列の次のタクシーにお乗りください。","*The* *next* *one*? *Thank* *you*.","次のですね。ありがとう。"),
("Have a pleasant evening in Doha.","ドーハでよい夜をおすごしください。","*Thank* *you*. *Good* *night*!","ありがとう。おやすみなさい！")],
[("this way","こちらへ"),("meter","メーター"),("cash","現金"),("in line","列にならんで"),("pleasant","心地よい")])
d('doh_metro','Doha Metroの係員','dmetro','d_metro','空港の下にあるDoha Metroの駅。ぴかぴかの改札の前に、係員が立っている。',[
("Hello. Welcome to Doha Metro. Where are you going?","こんにちは。Doha Metroへようこそ。どちらへ行かれますか。","*To* *the* *city* *center*. *Which* *line* *do* *I* *take*?","街の中心へ。どの路線に乗ればいいですか。"),
("Take the Red Line to Msheireb. It is the main station.","レッドラインでムシェイレブへ。中心の駅です。","*The* *Red* *Line* *to* *Msheireb*. *Got* *it*.","レッドラインでムシェイレブですね。わかりました。"),
("Do you have a travel card?","乗車カードはお持ちですか。","*No*, *not* *yet*. *Where* *can* *I* *buy* *one*?","いいえ、まだです。どこで買えますか。"),
("At that machine. A day pass is good for all day.","あの機械です。1日乗車券なら1日中使えます。","*A* *day* *pass*, *then*. *How* *long* *does* *it* *take*?","では1日乗車券にします。どのくらいかかりますか。"),
("About twenty-five minutes. Trains come every few minutes.","25分ほどです。電車は数分おきに来ます。","*Perfect*. *Thank* *you* *for* *your* *help*!","完ぺきです。助かりました！")],
[("line","路線"),("main station","中心の駅"),("travel card","乗車カード"),("day pass","1日乗車券"),("every few minutes","数分おきに")])
