# -*- coding: utf-8 -*-
# 世界一周編 ナイロビ+賢者+券選び。会話は創作(5往復)。値段は架空。個人名なし。実在名: Java House / Artcaffe / Safaricom / Pride Lounge / Jomo Kenyatta Intl / Villa Rosa Kempinski / Turkish Airlines / Qatar Airways
D=[]
import window_data as W
def d(id,who,bg,sp,intro,pairs,words,**kw):
    D.append(dict(id=id,who=who,bg=bg,sp=sp,intro=intro,pairs=pairs,words=words,**kw))

# ---- 達人賢者 ----
d('sage_1','達人賢者','sage','sage','星の見える広間。達人賢者が、旅のはじまりを教えてくれる。',[
("Welcome, travelers. You want to go around the world?","ようこそ、旅人たち。世界一周をしたいのですか。","*Yes*! *We* *want* to *see* *many* *airports*.","はい。たくさんの空港を見たいです。"),
("Good. One ticket can take you to many countries.","よい。1枚の航空券で、たくさんの国へ行けます。","*Really*? *How* *does* it *work*?","本当ですか。どうやって使うのですか。"),
W.OT("You choose a group of airlines. Then you fly from city to city, always going the same way around the earth.","航空会社のグループを選びます。そして、地球をいつも同じ向きに回りながら、都市から都市へ飛びます。",[
    W.O("start","Where do we start?","どこから始めますか。",card="どこから？",ico="🗺️",
        rep=("Good question. Let me tell you.","いい質問ですね。教えましょう。")),
    W.O("airline","Which airline should we choose?","どの航空会社を選べばいいですか。",card="航空会社",ico="✈️",
        rep=("Good question. You will choose at the ticket desk. First, the start.","いい質問です。航空券の窓口で選びます。まずは出発地です。"))],
    cards=1, fork={'tw':['airline']}),
("Your first stop is Nairobi, in Kenya. It is a good place to practice.","最初の寄港地はケニアのナイロビです。練習にぴったりの場所です。","*Nairobi*! *Is* it *far*?","ナイロビ！遠いですか。"),
("It is a long flight. But do not worry. Speak slowly, and smile.","長い飛行です。でも心配はいりません。ゆっくり話して、笑顔でいなさい。","*Thank* you. *We* *will* *try*!","ありがとうございます。がんばります。")],
[("round the world","世界一周"),("ticket","航空券"),("airline","航空会社"),("practice","練習する"),("slowly","ゆっくり")],conv=1,flow2=1)
d('sage_2','達人賢者','sage','sage','達人賢者に、航空券のえらび方をきいてみよう。',[
("Do you know the two big groups of airlines?","航空会社の大きなグループを2つ知っていますか。","*No*, *I* *don't*. *Please* *tell* me.","いいえ。教えてください。"),
W.OT("They are Star Alliance and oneworld. Each group has many airlines.","スターアライアンスとワンワールドです。どちらもたくさんの航空会社があります。",[
    W.O("diff","What's the difference?","何がちがうのですか。",card="ちがい",ico="🔍",
        rep=("Let me explain.","説明しましょう。")),
    W.O("pop","Which one is more popular?","どちらが人気ですか。",card="人気",ico="⭐",
        rep=("Both are very popular. Many travelers love them.","どちらもとても人気です。多くの旅人が好んでいます。"))],
    cards=1, fork={'tw':['alliance']}),
("The airlines are different, so the routes are different. Which one suits you depends on how you travel.","航空会社がちがうので、ルートもちがいます。どちらが合うかは、あなたの旅の仕方で決まります。","*Can* I *change* my *mind* *later*?","あとで気が変わってもいいですか。"),
("Choose one for this trip. You can choose the other one next time.","この旅ではひとつ選びます。もうひとつは、次の機会に選べます。","*But* *how* *do* *we* *know* *which* *one* *suits* *us*?","でも、どちらが私たちに合うか、どうやってわかりますか。"),
("Go to the ticket desk and talk it over well. Tell them how you want to travel.","航空券の窓口へ行って、よく相談しなさい。どんな旅をしたいか、伝えるのです。","*Okay*. *We'll* *go* *and* *talk* *with* *them* *now*!","わかりました。これから窓口で相談してきます。")],
[("alliance","航空会社の連合"),("route","ルート"),("suit","合う"),("change my mind","気が変わる"),("ticket desk","航空券の窓口")],conv=1,flow2=1)
d('sage_3','達人賢者','sage','sage','達人賢者から、旅の英語のコツをきこう。',[
("Here is a secret about travel English. Short is good.","旅の英語のひみつを教えましょう。短くて大丈夫です。","*Short* *is* *good*? *Really*?","短くていいのですか。本当に？"),
W.OT("Yes. Say 'Excuse me,' then say what you need. People will help you.","はい。『すみません』と言ってから、必要なことを言う。人は助けてくれます。",[
    W.O("dont","What if I don't understand?","わからなかったらどうしますか。",card="わからない時",ico="❓",
        rep=("Good question. There is a nice phrase.","いい質問です。いいフレーズがあります。")),
    W.O("polite","How can I be polite?","どうすれば丁寧になりますか。",card="丁寧に",ico="🙂",
        rep=("Good thinking. Politeness is a big help.","いい考えです。丁寧さは大きな助けになります。"))],
    cards=1, fork={'tw':['excuse me']}),
("Say, 'Could you say that again, please?' It is very polite.","『もう一度言っていただけますか』と言いなさい。とても丁寧です。","*Could* *you* *say* *that* *again*, *please*?","もう一度言っていただけますか。"),
("Perfect! And if it is too fast, say, 'Slowly, please.'","完璧です。それでも速すぎたら、『ゆっくりお願いします』と。","*Slowly*, *please*. *I* *can* *do* *that*.","ゆっくりお願いします。できそうです。"),
("You are ready. Now, go and choose your ticket.","準備はできました。さあ、航空券を選びに行きなさい。","*Thank* *you*, *wise* *teacher*!","ありがとうございます、賢者さま。")],
[("excuse me","すみません"),("polite","丁寧な"),("again","もう一度"),("understand","理解する"),("ready","準備ができた")],conv=1,flow2=1)

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
W.OT("Do you have your eTA for Kenya?","ケニアのeTA（電子渡航認証）はありますか。",[
    W.O("phone","Yes. I have it on my phone.","はい。スマホに入っています。",card="スマホ",ico="📱",
        rep=("Thank you. A phone is fine.","ありがとうございます。スマホで大丈夫です。")),
    W.O("paper","Yes. I have a paper copy.","はい。紙に印刷したものがあります。",card="紙",ico="📄",
        rep=("Thank you. Paper is fine, too.","ありがとうございます。紙も大丈夫です。"))],
    cards=1, fork={'tw':['eTA']}),
("Good. Please look at the camera.","結構です。カメラを見てください。","*Like* *this*?","こうですか。"),
("Yes, that is fine. Now, put your finger here.","はい、それでけっこうです。では、ここに指を置いてください。","*Okay*. *Is* *this* *right*?","はい。これでいいですか。"),
("All done. Welcome to Kenya!","終わりです。ケニアへようこそ。","*Thank* *you*! *Asante*!","ありがとう！アサンテ！")],
[("eTA","電子渡航認証"),("passport","パスポート"),("camera","カメラ"),("finger","指"),("welcome","ようこそ")],conv=1,flow2=1)
d('nbo_immig2','入国審査の係官','immig','officer2','別の窓口。係官は笑顔で、ゆっくり話してくれる。',[
W.OT("Hello. What is the purpose of your visit?","こんにちは。訪問の目的は何ですか。",[
    W.O("tour","I'm a tourist. I'm on a trip around the world.","観光です。世界一周の旅の途中です。",card="観光",ico="📷",
        rep=("A tourist! Welcome.","観光ですね！ようこそ。")),
    W.O("world","I'm traveling around the world.","世界一周をしています。",card="世界一周",ico="🌏",
        rep=("Around the world! That is a long trip.","世界一周ですか！長い旅ですね。"))],
    cards=1, fork={'tw':['purpose']}),
("Wonderful! How long will you stay in Kenya?","すばらしい。ケニアにはどのくらい滞在しますか。","*For* *three* *days*.","3日間です。"),
("Where will you stay in Nairobi?","ナイロビではどこに泊まりますか。","*At* *the* *Villa* *Rosa* *Kempinski*.","ヴィラ・ローザ・ケンピンスキーです。"),
("Do you have a ticket to leave Kenya?","ケニアを出る航空券はありますか。","*Yes*. *I* *fly* *out* *in* *three* *days*.","はい。3日後に出発します。"),
("Good. Enjoy your stay. Karibu Kenya!","結構です。滞在を楽しんで。ようこそケニアへ！","*Thank* *you*. *I* *will*!","ありがとうございます。楽しみます。")],
[("purpose","目的"),("tourist","観光客"),("stay","滞在する"),("hotel","ホテル"),("leave","出発する")],conv=1,flow2=1)
d('nbo_bag1','同じ便の旅行者','baggage','traveler','手荷物受け取り。ベルトがまわっている。自分のスーツケースをさがそう。',[
("Excuse me. Is this the belt for the flight from Tokyo?","すみません。ここは東京からの便のベルトですか。","*Yes*. *The* *sign* *says* *number* *three*.","はい。看板に3番と書いてあります。"),
("Great, thank you. What does your suitcase look like?","よかった、ありがとう。あなたのスーツケースはどんな形ですか。","*It's* *blue*, *with* *a* *yellow* *tag*.","青で、黄色いタグがついています。"),
("Look! Is that one yours? The blue one, next to the green board.","見て！あれですか。緑の板のとなりの青いの。","*Yes*, *that's* *mine*! *Excuse* *me*, *I* *will* *get* *it*.","はい、私のです！すみません、取ってきます。"),
W.OT("Careful, it is heavy. Do you need some help?","気をつけて、重いですよ。手伝いましょうか。",[
    W.O("no","No, thank you. I got it!","いいえ、大丈夫です。取れました！",card="大丈夫",ico="👍",
        rep=("Strong! Good job.","力持ちですね！いいですよ。")),
    W.O("yes","Yes, please. Can you help me?","はい、お願いします。手伝ってもらえますか。",card="お願い",ico="🙏",
        rep=("Sure. Here you go.","もちろん。どうぞ。"))],
    cards=1, fork={'tw':['help']}),
("Wonderful. Welcome to Kenya, and enjoy your trip!","よかった。ケニアへようこそ、旅を楽しんで。","*Thank* *you*! *You* *too*!","ありがとう！あなたも！")],
[("belt","ベルトコンベア"),("suitcase","スーツケース"),("tag","タグ"),("heavy","重い"),("help","手伝う")],conv=1,flow2=1)
d('nbo_bag2','手荷物受け取りのスタッフ','baggage','bag_staff2','スーツケースを受け取ったところで、係の人に声をかけられた。',[
W.OT("Welcome to Kenya. Do you have any plastic bags in your suitcase?","ケニアへようこそ。スーツケースにレジ袋は入っていますか。",[
    W.O("none","No, I don't have any.","いいえ、持っていません。",card="ない",ico="🙅",
        rep=("Good. That makes it easy.","よかった。それなら簡単です。")),
    W.O("why","Plastic bags? Why?","レジ袋ですか。なぜですか。",card="なぜ？",ico="❓",
        rep=("Good question. Let me explain.","いい質問です。説明しましょう。"))],
    cards=1, fork={'tw':['plastic bag']}),
("In Kenya, single-use plastic bags are not allowed. We use paper or cloth bags.","ケニアでは、使い捨てのレジ袋は禁止されています。紙か布の袋を使います。","*I* *see*. *I* *have* *a* *cloth* *bag*.","なるほど。布の袋ならあります。"),
("That is perfect. Please keep using it during your trip.","それは完璧です。旅の間、それを使ってください。","*Of* *course*. *Is* *the* *airport* *clean*?","もちろんです。空港はきれいですか。"),
("Yes, we try to keep Kenya clean and green.","はい、ケニアをきれいで緑豊かに保つようにしています。","*That's* *wonderful*.","すばらしいですね。"),
("Thank you for helping. Enjoy your trip!","協力ありがとうございます。旅を楽しんで。","*Thank* *you*. *Have* *a* *nice* *day*!","ありがとうございます。よい一日を。")],
[("plastic bag","レジ袋"),("allowed","許可されている"),("cloth","布"),("clean","きれいな"),("keep","保つ")],conv=1,flow2=1)
d('nbo_sim1','Safaricomの店員','sim','sim_staff','到着ロビーの Safaricom の店。現地のSIMカードを買おう。',[
("Jambo! Welcome to Safaricom. How can I help?","ジャンボ！Safaricomへようこそ。ご用件は何ですか。","*I* *need* *a* *SIM* *card*, *please*.","SIMカードがほしいです。"),
("Sure. May I see your passport? We must register your SIM.","かしこまりました。パスポートを見せてください。SIMの登録が必要です。","*Here* *is* *my* *passport*.","パスポートです。"),
("Thank you. Do you want data for seven days?","ありがとうございます。7日間のデータはいかがですか。","*Yes*. *How* *much* *data* *is* *it*?","はい。データ量はどのくらいですか。"),
W.OT("Five gigabytes. It costs one thousand shillings.","5ギガバイトです。料金は1000シリングです。",[
    W.O("card","Can I pay by card?","カードで払えますか。",card="カード",ico="💳",
        rep=("Yes, card is fine.","はい、カードで大丈夫です。")),
    W.O("cash","I will pay in cash.","現金で払います。",card="現金",ico="💵",
        rep=("Cash is fine, too.","現金も大丈夫ですよ。")),
    W.O("mpesa","What is M-Pesa?","M-Pesaって何ですか。",card="M-Pesa",ico="📱",
        then=dict(n="It is Safaricom's money on your phone. Everyone in Kenya uses it. Would you like to pay with it?",
                  jp="Safaricomの、携帯の中のお金です。ケニアではみんな使っています。それで払いますか。",
                  y=W.star("Yes, I will pay with M-Pesa."), yjp="はい、M-Pesaで払います。",
                  rep={'n': "Great. Just send it from your phone.", 'jp': "いいですね。スマホから送ってください。"}))],
    cards=1, fork={'tw':['gigabyte']}),
("Perfect. Your SIM is ready. Enjoy Kenya!","ばっちりです。SIMの準備ができました。ケニアを楽しんで。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("SIM card","SIMカード"),("register","登録する"),("data","データ通信"),("gigabyte","ギガバイト"),("pay by card","カードで払う")],conv=1,flow2=1)
d('nbo_sim2','Safaricomの店員','sim','sim_staff2','別の店員さん。スマホの設定がうまくいかないようだ。',[
("Hello. Is your phone working?","こんにちは。スマホは動いていますか。","*No*. *I* *can't* *use* *the* *internet*.","いいえ。インターネットが使えません。"),
("Let me see. Please turn your phone off and on again.","見てみましょう。スマホの電源を切って、また入れてください。","*Okay*. *Wait* *a* *moment*.","わかりました。少し待ってください。"),
W.OT("Do you see the signal bars now?","電波のバーが見えますか。",[
    W.O("four","Yes! I see four bars.","はい！4本立っています。",card="4本",ico="📶",
        rep=("Great. That is a strong signal.","いいですね。強い電波です。")),
    W.O("one","I see only one bar.","1本しか立っていません。",card="1本",ico="📶",
        rep=("Okay. That is enough to try.","わかりました。試すには十分です。"))],
    cards=1, fork={'tw':['signal']}),
("Good. Now open your browser and try a website.","よかった。ブラウザを開いて、サイトを見てみてください。","*It* *works*! *Thank* *you* *so* *much*.","つながりました！ありがとうございます。"),
("You are welcome. You can also use M-Pesa for payments here.","どういたしまして。ここではM-Pesaでの支払いも使えますよ。","*Great*. *I'll* *remember* *that*.","いいですね。覚えておきます。")],
[("internet","インターネット"),("turn off","電源を切る"),("signal","電波"),("browser","ブラウザ"),("payment","支払い")],conv=1,flow2=1)
d('nbo_taxi1','タクシー乗り場の係員','taxi','taxi_staff','空港の外。ホテルまでどうやって行こう。',[
("Hello, my friend. Do you need a taxi?","こんにちは。タクシーが必要ですか。","*Yes*. *Please*. *To* *the* *Villa* *Rosa* *Kempinski*.","はい、お願いします。ヴィラ・ローザ・ケンピンスキーまで。"),
("Sure. Please wait in this line. The next car is yours.","かしこまりました。この列でお待ちください。次の車があなたたちのです。","*How* *much* *is* *it*, *please*?","料金はいくらですか。"),
W.OT("It is a fixed price. Three thousand shillings to the city.","定額です。市内まで3000シリングです。",[
    W.O("card","Okay. Can I pay by card?","わかりました。カードで払えますか。",card="カード",ico="💳",
        rep=("Yes, card is fine.","はい、カードで大丈夫です。")),
    W.O("cash","Okay. I will pay in cash.","わかりました。現金で払います。",card="現金",ico="💵",
        rep=("Cash is fine. Thank you.","現金で大丈夫です。ありがとう。"))],
    cards=1, fork={'tw':['fixed price']}),
("The ride takes about forty minutes. The traffic is busy in the morning.","乗車は約40分です。朝は道がこみます。","*That's* *fine*. *We're* *not* *in* *a* *hurry*.","けっこうです。急いでいません。"),
("Good. Here is your car. Please watch your step.","よかった。こちらがお車です。足元にご注意ください。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("taxi","タクシー"),("fixed price","定額"),("traffic","交通量"),("busy","混んでいる"),("in a hurry","急いでいる")],conv=1,flow2=1)
d('nbo_taxi2','ライドシェアの運転手','taxi','driver','Uber アプリで車を呼んだ。待ち合わせ場所に、車がやって来た。',[
("Hello! Are you the passengers for the hotel?","こんにちは！ホテルへ行くお客さんですか。","*Yes*, *that's* *us*. *Is* *this* *the* *Uber*?","はい、私たちです。Uberですか。"),
("Yes. May I have the last four numbers of your phone?","はい。電話番号の下4けたを教えてください。","*Sure*. *It's* *one*, *two*, *three*, *four*.","もちろん。1、2、3、4です。"),
("Perfect. Let me help with your suitcase.","ばっちりです。スーツケースをお持ちします。","*Thank* *you*. *It's* *a* *little* *heavy*.","ありがとう。少し重いんです。"),
W.OT("No problem. Do you want the air conditioner on?","問題ありません。エアコンはつけますか。",[
    W.O("on","Yes, please. A little cool.","はい、お願いします。少し涼しく。",card="つける",ico="❄️",
        rep=("Okay. Cool air coming.","はい。涼しい風を出しますね。")),
    W.O("off","No, thank you. The window is fine.","いいえ、けっこうです。窓で大丈夫です。",card="いらない",ico="🪟",
        rep=("No problem. Window it is.","問題ありません。窓にしましょう。"))],
    cards=1, fork={'tw':['air conditioner']}),
("Good. Sit back and enjoy the ride!","よし。ゆったり座って、ドライブを楽しんで。","*Thank* *you*. *Let's* *go*!","ありがとう。行きましょう！")],
[("passenger","乗客"),("suitcase","スーツケース"),("heavy","重い"),("air conditioner","エアコン"),("ride","乗ること")],conv=1,flow2=1)

# ---- 空港: ナイロビ ----
# タスク061(新しい会話の流れ・この場面だけ。flow2=1 がスイッチ): 店員が英語で話す → 選ぶのは1場面に1回だけ(支払い。日本語の短い単語カード)
#   → カードをタップしたら見本の英語が音声だけで流れる(文字なし) → カンペ(文字)が出て声に出す → 間違えたらボタンなしで自動おてほん→言い直し
#   → 発音の数値は出さず、通じたかは店員の反応で返す → 支払いは目に見える形で返す(払って、コーヒーとケーキが出てくる)。
#   M-Pesa は「知らないカード」: タップしても分からないまま進ませず、プレイヤーが「What is M-Pesa?」と聞く → 短い説明 → 支払い(then)。
# 裏の反応時間(カードを出してからタップするまで)の測定と持ち越し→夢(053)は見えない形で続く。fork=その一言に入っている今日の語。
# 前の版(053)にあった「ホットかアイスか」の分かれ目は、1場面1回の決まりでなくした(会話の流れの中の「アイスにしますか」に変更)。
d('nbo_java1','Java Houseの店員','cafeK','cafe_staff','Java House に入った。コーヒーのいい香り。',[
("Jambo! Welcome to Java House. What can I get you?","ジャンボ！Java Houseへようこそ。ご注文は？","*I'd* *like* *a* *latte*, *please*.","ラテをお願いします。"),
("Sure. Would you like it iced? And a slice of cake with it?","かしこまりました。氷を入れますか。ケーキもひと切れいかがですか。","*Yes*, *iced*, *please*. *And* *a* *slice* *of* *cake*.","はい、アイスで。それとケーキをひと切れ。"),
("We have chocolate and carrot cake. Which one?","チョコレートとキャロットのケーキがあります。どちらにしますか。","*Carrot* *cake*, *please*.","キャロットケーキをお願いします。"),
W.OT("Okay. That is eight hundred shillings. How would you like to pay?","はい。800シリングです。お支払いはどうされますか。",[
    W.O('card',"Can I pay by card?","カードで払えますか。",card='カード払い',pay='card',
        rep=("Of course. Card is fine.","もちろん。カードで大丈夫です。")),
    W.O('cash',"Okay. I will pay in cash.","わかりました。現金で払います。",card='現金',pay='cash',
        rep=("Thank you. Cash is fine, too.","ありがとうございます。現金も大丈夫ですよ。")),
    W.O('mpesa',"What is M-Pesa?","M-Pesaって何ですか。",card='M-Pesa',pay='mpesa',
        then=dict(n="It is money on your phone. Everyone in Kenya uses it. Would you like to pay with it?",
                  jp="携帯の中のお金です。ケニアではみんな使っています。それで払いますか。",
                  y=W.star("Yes, I will pay with M-Pesa."), yjp="はい、M-Pesaで払います。",
                  rep={'n': "Great. Just tap your phone here.", 'jp': "いいですね。ここにスマホをかざしてください。"}))],
    cards=1, fork={'tw':['shillings']}),
("Here you go. Enjoy!","どうぞ。ごゆっくり。","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("latte","ラテ"),("iced","冷たい・氷入りの"),("slice","ひと切れ"),("carrot cake","キャロットケーキ"),("shillings","シリング(ケニアのお金)")],conv=1,flow2=1)
d('nbo_java2','となりのお客さん','cafeK','cafe_staff2','店は混んでいる。隣のお客さんが話しかけてきた。',[
("Excuse me. Is this seat free?","すみません。この席は空いていますか。","*Yes*, *it* *is*. *Please* *sit* *down*.","はい、空いています。どうぞ座ってください。"),
("Thank you. Are you traveling?","ありがとう。旅行中ですか。","*Yes*. *We* *are* *traveling* *around* *the* *world*.","はい。世界一周をしています。"),
("Wow! How do you like Nairobi so far?","わあ！ナイロビはここまでどうですか。","*It's* *great*. *The* *people* *are* *very* *kind*.","すばらしいです。人々がとても親切で。"),
W.OT("Thank you. You must try nyama choma before you leave.","ありがとう。帰る前にニャマチョマ（焼き肉）を食べてみて。",[
    W.O("try","I will try it. Thank you!","食べてみます。ありがとう！",card="食べてみる",ico="🍖",
        rep=("Good! It is grilled meat. You will love it.","いいですね！焼いたお肉です。きっと気に入りますよ。")),
    W.O("nyama","What is nyama choma?","ニャマチョマって何ですか。",card="ニャマチョマ",ico="🔥",
        then=dict(n="It is grilled meat. We eat it with friends. Would you like to try it?",
                  jp="焼いたお肉です。友だちと食べます。食べてみますか。",
                  y=W.star("Yes, I will try it."), yjp="はい、食べてみます。",
                  rep={'n': "Good! You will love it.", 'jp': "いいですね！きっと気に入りますよ。"}))],
    cards=1, fork={'tw':['grilled']}),
("It is our favorite. Enjoy your trip!","みんな大好きなんですよ。旅を楽しんで！","*I* *will*. *Thank* *you* *for* *the* *tip*!","そうします。教えてくれてありがとう！")],
[("seat","席"),("traveling","旅行している"),("kind","親切な"),("grilled","焼いた"),("tip","アドバイス・コツ")],kind='trav',conv=1,flow2=1)
d('nbo_art1','Artcaffeの店員','cafeK','cafe_staff3','Artcaffe に入った。パンのやけるにおいがする。',[
("Hello! Welcome to Artcaffe. Eat in or take away?","こんにちは！Artcaffeへようこそ。店内ですか、お持ち帰りですか。","*Eat* *in*, *please*.","店内でお願いします。"),
("Okay. Here is the menu. Would you like some water?","はい。こちらがメニューです。お水はいかがですか。","*Yes*, *please*. *What* *do* *you* *recommend*?","はい、お願いします。おすすめは何ですか。"),
W.OT("Our fresh bread and passion juice are popular.","焼きたてパンとパッションジュースが人気です。",[
    W.O("juice","I'll have the passion juice.","パッションジュースをください。",card="ジュース",ico="🧃",
        rep=("Nice. Very fresh.","いいですね。とても新鮮です。")),
    W.O("bread","I'll have the bread.","パンをください。",card="パン",ico="🍞",
        rep=("Nice. It is just baked.","いいですね。焼きたてです。")),
    W.O("both","I'll have the passion juice, and bread.","パッションジュースとパンをください。",card="どっちも",ico="🍽️",
        rep=("Nice. Both are popular.","いいですね。どちらも人気です。"))],
    cards=1, fork={'tw':['popular']}),
("Good choice. Anything else?","いい選択です。ほかには？","*That's* *all*, *thank* *you*.","以上です、ありがとう。"),
("Coming right up! Please sit anywhere.","すぐお持ちします！お好きな席へどうぞ。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("eat in","店内で食べる"),("take away","持ち帰り"),("recommend","おすすめする"),("passion juice","パッションフルーツのジュース"),("popular","人気のある")],conv=1,flow2=1)
d('nbo_art2','Artcaffeの店員','cafeK','cafe_staff4','お会計のとき、店員さんが話しかけてくれた。',[
("How was everything today?","今日はいかがでしたか。","*It* *was* *delicious*. *The* *bread* *was* *so* *soft*.","とてもおいしかったです。パンがやわらかくて。"),
("I am glad. Where are you from?","うれしいです。どちらから来ましたか。","*We* *are* *from* *Japan*.","日本からです。"),
("Japan! That is far. How long have you been traveling?","日本！遠いですね。旅はどのくらいですか。","*Only* *two* *days*. *This* *is* *our* *first* *stop*.","まだ2日です。ここが最初の寄港地です。"),
W.OT("Then you must see the animals. Nairobi National Park is close.","それなら動物を見なくちゃ。ナイロビ国立公園は近いですよ。",[
    W.O("go","Really? We would love to go.","本当ですか。ぜひ行きたいです。",card="行きたい",ico="🦒",
        rep=("Good. It is twenty minutes by car.","いいですね。車で20分です。")),
    W.O("far","Is it far?","遠いですか。",card="遠い？",ico="🚗",
        rep=("No, it is very close. Twenty minutes by car.","いいえ、とても近いです。車で20分です。"))],
    cards=1, fork={'tw':['close']}),
("Enjoy your trip! Come again soon.","旅を楽しんで！またいらしてくださいね。","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("delicious","おいしい"),("soft","やわらかい"),("far","遠い"),("national park","国立公園"),("close","近い")],conv=1,flow2=1)
d('nbo_lounge1','Pride Loungeの受付','lounge','lounge_staff','Pride Lounge に着いた。受付の人がにこやかに迎えてくれる。',[
("Welcome to the Pride Lounge. May I see your boarding pass?","Pride Loungeへようこそ。搭乗券を見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
("Thank you. Please enjoy the lounge. Do you need Wi-Fi?","ありがとうございます。どうぞお楽しみください。Wi-Fiは必要ですか。","*Yes*, *please*. *What's* *the* *password*?","はい、お願いします。パスワードは何ですか。"),
W.OT("It is on the card. Please connect to the lounge network.","カードに書いてあります。ラウンジのネットワークに接続してください。",[
    W.O("drink","Where can I get a drink?","飲み物はどこでもらえますか。",card="飲み物",ico="🥤",
        rep=("Sure. Let me show you.","もちろん。ご案内します。")),
    W.O("food","Where can I get some food?","食べ物はどこでもらえますか。",card="食べ物",ico="🍽️",
        rep=("Sure. Let me show you.","もちろん。ご案内します。"))],
    cards=1, fork={'tw':['connect']}),
("The bar is on the left. There is also food in the middle.","バーは左側です。中央には食事もあります。","*Great*. *Is* *there* *a* *quiet* *area*?","いいですね。静かな場所はありますか。"),
("Yes, at the back. Please relax and enjoy.","はい、奥にあります。ゆっくりくつろいでください。","*Thank* *you* *very* *much*.","ありがとうございます。")],
[("lounge","ラウンジ"),("password","パスワード"),("connect","接続する"),("quiet","静かな"),("relax","くつろぐ")],conv=1,flow2=1)
d('nbo_lounge2','ラウンジの隣の席のお客さん','lounge','lounge_guest','ラウンジのソファ。隣のお客さんが笑顔であいさつしてくれた。',[
("Hello! Are you leaving Kenya today?","こんにちは！今日ケニアを出発しますか。","*Yes*. *We* *fly* *to* *Doha* *soon*.","はい。もうすぐドーハへ飛びます。"),
("Safe travels! Did you enjoy your time here?","気をつけて！ここでの時間は楽しめましたか。","*Yes*. *We* *saw* *the* *giraffes*.","はい。キリンを見ました。"),
W.OT("Wonderful! Did you feed them?","すばらしい！えさをあげましたか。",[
    W.O("fed","Yes! They were very gentle.","はい！とてもおだやかでした。",card="あげた",ico="🥕",
        rep=("Great! They are gentle animals.","いいですね！おだやかな動物です。")),
    W.O("watched","No, I only watched them.","いいえ、見ただけです。",card="見ただけ",ico="👀",
        rep=("That is fine. Watching is fun, too.","それでもいいですよ。見るのも楽しいです。"))],
    cards=1, fork={'tw':['feed']}),
("Giraffes love snacks! Was it safe for you?","キリンはおやつが大好き！こわくなかったですか。","*Yes*. *I* *can't* *wait* *to* *come* *back*!","はい。また来るのが待ちきれません！"),
("Enjoy! Safari njema! That means good journey.","楽しんで！サファリ・ンジェマ！「よい旅を」という意味です。","*Safari* *njema*! *Thank* *you*!","サファリ・ンジェマ！ありがとう！")],
[("giraffe","キリン"),("feed","えさをあげる"),("safe","安全な"),("gentle","おだやかな"),("journey","旅")],kind='trav',conv=1,flow2=1)
d('nbo_duty1','免税店の店員','duty','duty_staff','免税店で、ケニアのコーヒーを見つけた。',[
("Welcome! Are you looking for something special?","いらっしゃいませ！何かお探しですか。","*Yes*. *I* *want* *Kenyan* *coffee* *for* *my* *family*.","はい。家族にケニアのコーヒーをおみやげにしたいです。"),
("Good choice. This one is from the mountains. It is very smooth.","いい選択です。これは山で育ったコーヒーです。とてもまろやかですよ。","*How* *much* *is* *it*?","いくらですか。"),
("It is twelve dollars for one bag.","1袋12ドルです。","*I'll* *take* *two* *bags*, *please*.","2袋ください。"),
W.OT("Two bags. Would you like a gift box?","2袋ですね。ギフトボックスはどうしますか。",[
    W.O("gift","Yes, please. It's a present.","はい、お願いします。プレゼントなので。",card="ギフト用",ico="🎁",
        rep=("Lovely. I will wrap it.","すてきです。包みますね。")),
    W.O("plain","No, thank you. A plain bag is fine.","いいえ、けっこうです。ふつうの袋で大丈夫です。",card="そのまま",ico="🛍️",
        rep=("No problem. Just the bags.","問題ありません。袋のままで。"))],
    cards=1, fork={'tw':['gift box']}),
("Done! Here is your receipt. Thank you!","できました！レシートです。ありがとうございます！","*Thank* *you*. *Asante*!","ありがとう。アサンテ！")],
[("coffee","コーヒー"),("smooth","まろやか"),("gift box","ギフトボックス"),("present","贈り物"),("receipt","レシート")],conv=1,flow2=1)
d('nbo_duty2','免税店の店員','duty','duty_staff2','隣の棚には、ケニアの紅茶と、カラフルな布がならんでいる。',[
("Hello! Would you like to try some Kenyan tea?","こんにちは！ケニアの紅茶を試してみませんか。","*Yes*, *please*. *It* *smells* *nice*.","はい、お願いします。いい香りです。"),
("Here you go. Be careful. It is hot.","どうぞ。気をつけて。熱いですよ。","*Mmm*, *it's* *delicious*. *Is* *it* *strong*?","おいしい。濃いですか。"),
("A little strong. Many people add milk and sugar.","少し濃いです。ミルクと砂糖を入れる人が多いですよ。","*I'll* *buy* *a* *box* *of* *tea*.","紅茶を1箱買います。"),
W.OT("Great. And this colorful cloth is a kikoi. Which color do you like?","いいですね。このカラフルな布は「キコイ」といいます。何色が好きですか。",[
    W.O("blue","It's beautiful. I'll take a blue one.","きれいですね。青いのをください。",card="青",ico="🟦",
        rep=("Lovely. Blue is a good choice.","すてきです。青はいい選択です。")),
    W.O("red","It's beautiful. I'll take a red one.","きれいですね。赤いのをください。",card="赤",ico="🟥",
        rep=("Lovely. Red is a good choice.","すてきです。赤はいい選択です。")),
    W.O("kikoi","What is a kikoi?","キコイって何ですか。",card="キコイ",ico="🧣",
        then=dict(n="It is a Kenyan cloth. People use it as a scarf, a skirt, or a towel. Which color do you like?",
                  jp="ケニアの布です。スカーフにも、スカートにも、タオルにもなります。何色が好きですか。",
                  y=W.star("I'll take a blue one."), yjp="青いのをください。",
                  rep={'n': "Lovely. Blue is a good choice.", 'jp': "すてきです。青はいい選択です。"}))],
    cards=1, fork={'tw':['colorful']}),
("Lovely. Thank you for shopping with us!","すてきです。お買い上げありがとうございます！","*Thank* *you*. *Have* *a* *good* *day*!","ありがとう。よい一日を！")],
[("tea","紅茶"),("strong","濃い"),("sugar","砂糖"),("colorful","カラフルな"),("beautiful","美しい")],conv=1,flow2=1)
d('nbo_gate1','搭乗ゲートの係員','gate','gate_agent','搭乗ゲートに着いた。アナウンスが流れている。',[
("Good afternoon. May I see your boarding pass and passport?","こんにちは。搭乗券とパスポートを見せていただけますか。","*Here* *you* *are*.","どうぞ。"),
W.OT("Thank you. Boarding will begin in twenty minutes.","ありがとうございます。搭乗は20分後に始まります。",[
    W.O("right","Is this the right gate?","ここで合っていますか。",card="ゲート",ico="🚪",
        rep=("Good question.","いい質問です。")),
    W.O("doha","Is this the correct gate for Doha?","ここはドーハ行きのゲートで合っていますか。",card="行き先",ico="🛫",
        rep=("Good question.","いい質問です。"))],
    cards=1, fork={'tw':['boarding']}),
("Yes, this is the correct gate. Please wait over there.","はい、このゲートで合っています。あちらでお待ちください。","*Can* *I* *buy* *a* *drink* *first*?","先に飲み物を買ってもいいですか。"),
("Of course. Just come back before boarding.","もちろん。搭乗前に戻ってくればだいじょうぶです。","*Thank* *you*. *I'll* *be* *back* *soon*.","ありがとう。すぐ戻ります。"),
("No problem. Have a safe flight!","問題ありません。よい旅を！","*Thank* *you*. *Goodbye*!","ありがとう。さようなら！")],
[("gate","搭乗ゲート"),("boarding","搭乗"),("correct","正しい"),("wait","待つ"),("flight","フライト")],conv=1,flow2=1)
d('nbo_gate2','搭乗ゲートの係員','gate','gate_agent2','ゲートの前に人がたくさん。次の都市へ出発する時間が近づいている。',[
("Attention please. Flight boarding is now open.","お知らせします。搭乗が始まりました。","*Excuse* *me*. *Can* *we* *board* *now*?","すみません。いま乗れますか。"),
W.OT("Which group are you in?","何番のグループですか。",[
    W.O("two","We are in group two.","グループ2です。",card="グループ2",ico="2️⃣",
        rep=("Group two. Thank you.","グループ2ですね。ありがとう。")),
    W.O("three","We are in group three.","グループ3です。",card="グループ3",ico="3️⃣",
        rep=("Group three. Thank you.","グループ3ですね。ありがとう。"))],
    cards=1, fork={'tw':['board']}),
("Your group will board in a few minutes. Please wait.","あなたのグループは数分後です。お待ちください。","*Okay*. *Is* *the* *flight* *on* *time*?","わかりました。フライトは定刻ですか。"),
("Yes, on time. You will like the view from the window.","はい、定刻です。窓からの景色を気に入りますよ。","*I* *love* *the* *view*. *I* *can't* *wait*.","景色が大好きです。待ちきれません。"),
("Your group, please come forward now. Enjoy your trip!","グループの方、どうぞお進みください。旅を楽しんで！","*Thank* *you*. *Goodbye*, *Nairobi*!","ありがとう。さようなら、ナイロビ！")],
[("attention","お知らせ"),("board","搭乗する"),("on time","定刻の"),("view","景色"),("come forward","前に進む")],conv=1,flow2=1)

# ---- 出発: ナイロビ(Qatar Airways でドーハへ) ----
# 実在名: Qatar Airways。飛行時間 約5時間(2026-11-14 確認、資料は5時間〜5時間20分)。重さ・時刻・席番号は架空。
d('nbo_checkin1','Qatar Airwaysのチェックイン係','checkinQ','qr_checkin','ナイロビの空港、Qatar Airwaysのカウンター。係の人が明るく手をふっている。',[
("Jambo! Welcome to Qatar Airways. Where are you flying today?","ジャンボ！カタール航空へようこそ。今日はどちらへ？","*Jambo*! *We* *are* *flying* *to* *Doha*.","ジャンボ！ドーハへ行きます。"),
("Lovely. Please put your suitcase on the scale.","いいですね。スーツケースをはかりにのせてください。","*Sure*. *Is* *it* *too* *heavy*?","はい。重すぎますか。"),
("No, it is fine. Is Doha your final stop today?","いいえ、大丈夫です。今日の最終目的地はドーハですか。","*Yes*. *We* *will* *stay* *in* *Doha* *for* *one* *night*.","はい。ドーハに1泊します。"),
W.OT("Then your bag goes to Doha. Here is your baggage tag.","では荷物はドーハまでです。こちらが手荷物の引換証です。",[
    W.O("time","Thank you. What time does boarding start?","ありがとう。搭乗は何時に始まりますか。",card="搭乗時間",ico="⏰",
        rep=("Good question.","いい質問です。")),
    W.O("gate","Thank you. Which gate is it?","ありがとう。何番ゲートですか。",card="ゲート",ico="🚪",
        rep=("Good question.","いい質問です。"))],
    cards=1, fork={'tw':['baggage tag']}),
("Boarding is forty minutes before the flight, at the gate on your pass. Have a good trip!","搭乗は出発の40分前、搭乗券に書かれたゲートです。よい旅を！","*Asante*! *Goodbye*, *Nairobi*!","アサンテ！さよなら、ナイロビ！")],
[("scale","はかり"),("heavy","重い"),("final stop","最終目的地"),("baggage tag","手荷物の引換証"),("boarding","搭乗")],conv=1,flow2=1)
d('nbo_checkin2','Qatar Airwaysのチェックイン係','checkinQ','qr_checkin2','となりのカウンター。係の人が、画面を見て少しこまった顔をしている。',[
("Good evening. Passports, please. Two passengers?","こんばんは。パスポートをお願いします。お二人ですか。","*Yes*, *two*. *Here* *are* *our* *passports*.","はい、二人です。パスポートです。"),
W.OT("Thank you. I am sorry, but your seats are not together.","ありがとうございます。すみません、お席がはなれています。",[
    W.O("together","Oh no. Can we sit together, please?","そんな。いっしょに座れますか。",card="いっしょに",ico="🪑",
        rep=("Of course. I will try.","もちろん。やってみます。")),
    W.O("next","Oh no. Can you put us next to each other?","そんな。となりどうしにできますか。",card="となり",ico="👫",
        rep=("Yes, I understand. I will try.","わかりました。やってみます。"))],
    cards=1, fork={'tw':['together']}),
("Let me check. One moment. I have two seats in row thirty.","お調べします。少々お待ちを。30列目に2席あります。","*Great*! *Is* *one* *of* *them* *a* *window* *seat*?","よかった！どちらかは窓側ですか。"),
("Yes. Thirty A is by the window, and thirty B is next to it.","はい。30Aが窓側で、30Bがそのとなりです。","*Perfect*. *We* *will* *take* *them*.","完ぺきです。その席にします。"),
("All done. Here are your new boarding passes.","できました。新しい搭乗券です。","*Thank* *you* *for* *your* *help*!","助かりました。ありがとう！")],
[("passenger","乗客"),("together","いっしょに"),("one moment","少々お待ちください"),("row","列"),("next to","〜のとなり")],conv=1,flow2=1)
d('nbo_sec1','保安検査の係員','security','sec_n1','保安検査の列。係員はてきぱきと、でもやさしく声をかけている。',[
W.OT("Next, please. Put your bags on the belt.","次の方どうぞ。荷物をベルトにのせてください。",[
    W.O("laptop","Okay. Do I take out my laptop?","はい。ノートパソコンは出しますか。",card="パソコン",ico="💻",
        rep=("Good question.","いい質問です。")),
    W.O("tablet","Okay. Do I take out my tablet?","はい。タブレットは出しますか。",card="タブレット",ico="📱",
        rep=("Good question.","いい質問です。"))],
    cards=1, fork={'tw':['laptop']}),
("Yes. Laptops and tablets go in a separate tray.","はい。パソコンとタブレットはべつのトレーに入れます。","*All* *right*. *What* *about* *my* *jacket*?","わかりました。上着はどうしますか。"),
("Jackets off, please. And your belt and watch.","上着はぬいでください。ベルトと時計もお願いします。","*Okay*. *Here* *is* *my* *belt*.","はい。ベルトです。"),
("Do you have any liquids in your bag?","かばんに液体は入っていますか。","*Only* *a* *small* *bottle* *of* *water*.","小さい水のボトルだけです。"),
("Sorry, you cannot take water through. Please empty the bottle.","すみません、水は持ちこめません。ボトルを空にしてください。","*I* *see*. *I* *will* *drink* *it* *now*.","わかりました。今飲みます。")],
[("laptop","ノートパソコン"),("separate","べつの"),("tray","トレー"),("liquids","液体"),("empty","空にする")],conv=1,flow2=1)
d('nbo_sec2','保安検査の係員','security','sec_n2','検査のあと、かばんが1つだけ横によけられた。係員が手まねきしている。',[
("Excuse me. Is this your bag?","すみません。これはあなたのかばんですか。","*Yes*, *it* *is* *mine*. *Is* *there* *a* *problem*?","はい、私のです。何か問題がありますか。"),
W.OT("I need to open it. Is that okay?","中を開けて見ます。よろしいですか。",[
    W.O("go","Sure. Go ahead.","はい。どうぞ。",card="どうぞ",ico="👍",
        rep=("Thank you.","ありがとう。")),
    W.O("why","Go ahead. Is there a problem?","どうぞ。何か問題がありますか。",card="なぜ？",ico="❓",
        rep=("No problem. Just a check.","問題ありません。ただの確認です。"))],
    cards=1, fork={'tw':['go ahead']}),
("What is this long thing?","この長いものは何ですか。","*It* *is* *a* *wooden* *giraffe*. *It* *is* *a* *souvenir*.","木のキリンです。おみやげです。"),
("Ah, a giraffe! Very nice. No problem.","ああ、キリンですね。すてきです。問題ありません。","*Thank* *you*. *Can* *I* *close* *my* *bag*?","ありがとう。かばんを閉めてもいいですか。"),
("Yes. You are good to go. Have a safe flight.","はい。行って大丈夫です。安全な空の旅を。","*Thanks*. *Have* *a* *nice* *day*!","ありがとう。よい一日を！")],
[("problem","問題"),("go ahead","どうぞ"),("wooden","木の"),("souvenir","おみやげ"),("safe flight","安全な空の旅")],conv=1,flow2=1)
d('nbo_plane1','Qatar Airwaysの客室乗務員','cabinQ','qr_crew','ついに機内へ。客室乗務員が、おだやかな声でむかえてくれた。',[
("Good evening. Welcome aboard. May I see your boarding pass?","こんばんは。ご搭乗ありがとうございます。搭乗券を見せていただけますか。","*Good* *evening*. *Here* *it* *is*.","こんばんは。これです。"),
("Thirty A. Go down this aisle. It is on your left.","30Aですね。この通路を進んでください。左側です。","*Thank* *you*. *Is* *there* *space* *for* *my* *bag*?","ありがとう。かばんを入れる場所はありますか。"),
("Yes, in the overhead bin. Let me help you.","はい、頭上の荷物入れに。お手伝いします。","*That* *is* *very* *kind*. *Thank* *you*.","ご親切にどうも。ありがとう。"),
W.OT("My pleasure. Would you like water or juice before takeoff?","どういたしまして。離陸の前に、水かジュースはいかがですか。",[
    W.O("water","Water, please.","水をお願いします。",card="水",ico="💧",
        rep=("Water. Coming right up.","お水ですね。すぐお持ちします。")),
    W.O("juice","Juice, please.","ジュースをお願いします。",card="ジュース",ico="🧃",
        rep=("Juice. Coming right up.","ジュースですね。すぐお持ちします。")),
    W.O("blanket","Water, please. And may I have a blanket?","水をお願いします。毛布もいただけますか。",card="水と毛布",ico="🛏️",
        rep=("Water and a blanket. Coming right up.","お水と毛布ですね。すぐお持ちします。"))],
    cards=1, fork={'tw':['takeoff']}),
("The flight to Doha takes about five hours. Please relax.","ドーハまでは約5時間です。ゆっくりおくつろぎください。","*Great*. *Goodbye*, *Nairobi*!","いいですね。さよなら、ナイロビ！")],
[("aboard","搭乗して"),("aisle","通路"),("overhead bin","頭上の荷物入れ"),("takeoff","離陸"),("blanket","毛布")],conv=1,flow2=1)
d('nbo_plane2','Qatar Airwaysの客室乗務員','cabinQ','qr_crew2','雲の上。食事のカートが、しずかに近づいてきた。',[
("Excuse me. Chicken with rice, or vegetable pasta?","失礼します。チキンとライス、または野菜のパスタ、どちらになさいますか。","*Sorry*, *could* *you* *say* *that* *again*?","すみません、もう一度言ってもらえますか。"),
W.OT("Of course. Chicken with rice, or vegetable pasta?","もちろんです。チキンとライス、または野菜のパスタです。",[
    W.O("chicken","Chicken with rice, please.","チキンとライスをお願いします。",card="チキン",ico="🍗",
        rep=("Good choice.","いい選択です。")),
    W.O("pasta","Vegetable pasta, please.","野菜のパスタをお願いします。",card="パスタ",ico="🍝",
        rep=("Good choice.","いい選択です。"))],
    cards=1, fork={'tw':['vegetable']}),
("Certainly. And something to drink?","かしこまりました。お飲み物はいかがですか。","*Do* *you* *have* *hot* *tea*?","温かい紅茶はありますか。"),
("Yes, we do. With milk and sugar?","はい、ございます。ミルクと砂糖は入れますか。","*Just* *milk*, *please*.","ミルクだけお願いします。"),
("Here you are. We will land in Doha in two hours.","どうぞ。あと2時間でドーハに着陸します。","*Thank* *you*. *I* *can't* *wait*!","ありがとう。待ちきれません！")],
[("say that again","もう一度言う"),("vegetable","野菜"),("something to drink","飲み物"),("sugar","砂糖"),("land","着陸する")],conv=1,flow2=1)

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
d('doh_bag2','となりの旅行者','dbag','d_traveler','ベルトの前。同じ青いスーツケースに、となりの人も手をのばした。',[
("Excuse me, I think this blue suitcase is mine.","すみません、この青いスーツケースは私のだと思います。","*Sorry*, *but* *I* *think* *it* *is* *ours*. *Look* *at* *the* *name* *tag*.","すみません、私たちのだと思います。名札を見てください。"),
("Oh! You are right. It is not my name. I am so sorry.","あっ！そのとおりです。私の名前ではありません。本当にごめんなさい。","*That's* *okay*. *They* *look* *the* *same*.","大丈夫です。そっくりですから。"),
("Mine has a red ribbon on the handle.","私のは、持ち手に赤いリボンがついています。","*A* *red* *ribbon*? *I* *see* *one* *over* *there*!","赤いリボン？あそこに1つ見えます！"),
("Yes, that is mine! Thank you so much.","そう、あれが私のです！本当にありがとう。","*You're* *welcome*. *Where* *are* *you* *from*?","どういたしまして。どちらからですか。"),
("I live in Doha now. I just came back from Nairobi. Welcome!","いまはドーハに住んでいます。ナイロビから帰ってきたところです。ようこそ！","*Thank* *you*! *Have* *a* *good* *night*.","ありがとう！おやすみなさい。")],
[("mine","私のもの"),("name tag","名札"),("the same","同じ"),("ribbon","リボン"),("handle","持ち手")],kind='trav')
d('doh_sim1','Ooredooの店員','dsim','d_sim','到着ロビーのOoredoo。店員は手ぎわがよく、話もはやい。',[
("Welcome to Ooredoo. How can I help you today?","Ooredooへようこそ。ご用件は何でしょうか。","*Hello*. *I* *need* *a* *SIM* *card* *for* *one* *day*.","こんにちは。1日だけ使うSIMカードがほしいです。"),
("We have a visitor SIM. It is good for seven days.","旅行者用のSIMがあります。7日間使えます。","*Seven* *days* *is* *fine*. *How* *much* *is* *it*?","7日間でいいです。いくらですか。"),
("It is thirty riyals. May I have your passport?","30リヤルです。パスポートをお借りできますか。","*Here* *you* *are*. *Can* *I* *pay* *by* *card*?","どうぞ。カードで払えますか。"),
("Yes, card is fine. I will set it up for you.","はい、カードで大丈夫です。こちらで設定します。","*Thank* *you*. *Does* *it* *work* *now*?","ありがとう。もう使えますか。"),
("Yes, it is ready. Enjoy your stay in Doha.","はい、準備できました。ドーハでの滞在を楽しんで。","*That* *was* *fast*! *Thank* *you*.","はやい！ありがとう。")],
[("visitor","訪問者"),("riyal","リヤル(カタールのお金)"),("pay by card","カードで払う"),("set up","設定する"),("ready","準備ができた")])
d('doh_sim2','カウンターの列のとなりの人','dsim','d_sim2','SIMを入れたのに、地図が開かない。Ooredooのカウンターの列で、となりの人が声をかけてくれた。',[
("You look worried. Is something wrong with your phone?","心配そうですね。スマホに何かありましたか。","*Yes*. *The* *internet* *does* *not* *work*.","はい。インターネットがつながりません。"),
("I had the same problem once. May I look at it?","私も前に同じことがありました。見てもいいですか。","*Sure*. *Here* *it* *is*.","はい。どうぞ。"),
("Ah. Mobile data is off. I will turn it on.","ああ。モバイルデータがオフです。オンにしますね。","*Oh*, *I* *see*. *Is* *it* *working* *now*?","そうだったんですね。もう動いていますか。"),
("Yes. Please open a map and try.","はい。地図を開いて試してください。","*It* *works*! *I* *can* *see* *the* *map*.","つながった！地図が見えます。"),
("Good. Next time, check that setting first.","よかったです。次は、まずその設定を見てくださいね。","*I* *will*. *Thank* *you* *for* *your* *help*.","そうします。助かりました。")],
[("internet","インターネット"),("mobile data","モバイルデータ通信"),("turn on","オンにする"),("try","試す"),("setting","設定")],kind='trav')
d('doh_taxi','Karwaタクシーの係員','dtaxi','d_taxi','到着ロビーのはしにあるタクシー乗り場。係員が、しずかに手で列を案内している。',[
("Good evening. Taxi? This way, please.","こんばんは。タクシーですか。こちらへどうぞ。","*Yes*, *please*. *We* *are* *going* *to* *Souq* *Waqif*.","お願いします。スーク・ワキーフへ行きます。"),
("Souq Waqif. It takes about twenty minutes.","スーク・ワキーフですね。20分ほどです。","*Good*. *Does* *the* *taxi* *use* *a* *meter*?","よかった。タクシーはメーターを使いますか。"),
("Yes, all Karwa taxis use a meter.","はい、Karwaのタクシーはすべてメーター制です。","*Can* *I* *pay* *by* *card*?","カードで払えますか。"),
("Yes, card or cash. Please take the next taxi in line.","はい、カードでも現金でも。列の次のタクシーにお乗りください。","*The* *next* *one*? *Thank* *you*.","次のですね。ありがとう。"),
("Have a pleasant evening in Doha.","ドーハでよい夜をおすごしください。","*Thank* *you*. *Good* *night*!","ありがとう。おやすみなさい！")],
[("this way","こちらへ"),("meter","メーター"),("cash","現金"),("in line","列にならんで"),("pleasant","心地よい")])
d('doh_metro','改札の前のとなりの乗客','dmetro','d_metrop','空港の下にあるDoha Metroの駅。ぴかぴかの改札の前で、となりの乗客が声をかけてくれた。',[
("Hello. Are you going into the city?","こんにちは。街へ行かれるのですか。","*Yes*. *To* *the* *city* *center*. *Which* *line* *do* *I* *take*?","はい。街の中心へ。どの路線に乗ればいいですか。"),
("Take the Red Line to Msheireb. It is the main station.","レッドラインでムシェイレブへ。中心の駅です。","*The* *Red* *Line* *to* *Msheireb*. *Got* *it*.","レッドラインでムシェイレブですね。わかりました。"),
("Do you have a travel card?","乗車カードはお持ちですか。","*No*, *not* *yet*. *Where* *can* *I* *buy* *one*?","いいえ、まだです。どこで買えますか。"),
("At this machine. A day pass is good for all day.","この機械です。1日乗車券なら1日中使えます。","*A* *day* *pass*, *then*. *How* *long* *does* *it* *take*?","では1日乗車券にします。どのくらいかかりますか。"),
("About twenty-five minutes. Trains come every few minutes.","25分ほどです。電車は数分おきに来ます。","*Perfect*. *Thank* *you* *for* *your* *help*!","完ぺきです。助かりました！")],
[("line","路線"),("main station","中心の駅"),("travel card","乗車カード"),("day pass","1日乗車券"),("every few minutes","数分おきに")],kind='trav')

# ---- 窓口（タスク012）: 宣言・聞き取り5本・線を引く・値段・読み上げ確認・名前の確認 ----
import window_data
window_data.add(D)

# ---- 割りこみ・顔なじみ・持ち越し（タスク014。設計 005）----
import event_data
event_data.add(D)

# ---- ドーハ後半: 市内16＋出発8（タスク023。設計 018 案A）。国ごとのデータは別ファイル ----
import doha_data
doha_data.add(D)

# ---- 1日目の羽田出発(タスク043): チェックイン・保安検査・出国・出発ゲート・搭乗・機内。会話は仮 ----
import haneda_data
haneda_data.add(D)

# ---- 1日目の最初の長距離便(タスク048): CAに頼まれて機内アナウンスを読み、食事のあとに自分の声が機内放送で流れる ----
import pa_data
pa_data.add(D)

# ---- ナイロビの滞在(観光): サファリ・マサイマーケット(タスク058)。会話は 053 の分かれ目の型 ----
import stay_data
stay_data.add(D)

# ---- ロヴァニエミの到着まわり(タスク065): 入国審査・手荷物・到着ロビー・無料Wi-Fi・バス乗り場。会話は 053 の分かれ目の型 ----
import rvn_data
rvn_data.add(D)
import rvn_stay_data
rvn_stay_data.add(D)

# ---- 英会話カフェ(タスク068・試作): ナイロビの小さな英会話カフェで先生と予行練習。チェックモードからだけ入る ----
import eikaiwa_data
eikaiwa_data.add(D)
import camp_data   # タスク078: 合宿(マッチョルル教室)デモ版。チェックモードからだけ入る
camp_data.add(D)
