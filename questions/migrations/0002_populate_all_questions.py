from django.db import migrations

def add_questions(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    Choice = apps.get_model('questions', 'Choice')

    # Clear existing questions to avoid duplicates
    Question.objects.all().delete()

    # Section 1: Kişisel Bilgiler
    Question.objects.create(text="İsim Soyisim", section=1, q_type="open_ended")
    Question.objects.create(text="Doğum Tarihi + Doğum Saati (Burç Bilgisi İçin)", section=1, q_type="datetime")
    q_cinsiyet = Question.objects.create(text="Cinsiyet", section=1, q_type="single_choice_other")
    Choice.objects.create(question=q_cinsiyet, text="Kadın")
    Choice.objects.create(question=q_cinsiyet, text="Erkek")
    q_yonelim = Question.objects.create(text="Yönelim", section=1, q_type="multiple_choice_other")
    Choice.objects.create(question=q_yonelim, text="Heteroseksüel")
    Choice.objects.create(question=q_yonelim, text="Homoseksüel")
    Choice.objects.create(question=q_yonelim, text="Biseksüel")
    Choice.objects.create(question=q_yonelim, text="Panseksüel")
    Choice.objects.create(question=q_yonelim, text="Aseksüel")
    q_iliski_durumu = Question.objects.create(text="İlişki Durumu", section=1, q_type="multiple_choice_single")
    Choice.objects.create(question=q_iliski_durumu, text="İlişkim yok")
    Choice.objects.create(question=q_iliski_durumu, text="İlişkim var")
    Choice.objects.create(question=q_iliski_durumu, text="Karmaşık")
    Question.objects.create(text="IG Nickname", section=1, q_type="open_ended")
    Question.objects.create(text="Gittiğiniz Okul, Bölüm ve Yılınız", section=1, q_type="multi_text")
    Question.objects.create(text="Nerede Oturuyorsun?", section=1, q_type="open_ended")
    Question.objects.create(text="Kullandığınız Sosyal Medya Platformları", section=1, q_type="open_ended")
    Question.objects.create(text="Varsa İçinde Bulunduğun Kulüpler/Topluluklar", section=1, q_type="open_ended")
    Question.objects.create(text="En Sevdiğin Filmler", section=1, q_type="open_ended")
    Question.objects.create(text="En Sevdiğin Diziler", section=1, q_type="open_ended")
    Question.objects.create(text="En Sevdiğin Şarkılar", section=1, q_type="open_ended")
    Question.objects.create(text="En Sevdiğin Müzisyenler", section=1, q_type="open_ended")
    Question.objects.create(text="En Sevdiğin Enstrüman", section=1, q_type="open_ended")
    Question.objects.create(text="Sevgilinle El Eleyken Dinlemek İsteyeceğin Müzikler", section=1, q_type="open_ended")

    # Section 2: İlişki Tercihleri
    q_eslestirilmek = Question.objects.create(text="Biriyle Eşleştirilmek İstiyor Musunuz?", section=2, q_type="multiple_choice_single")
    Choice.objects.create(question=q_eslestirilmek, text="Evet")
    Choice.objects.create(question=q_eslestirilmek, text="Hayır")
    q_nasil_iliski = Question.objects.create(text="Nasıl Bir İlişki Arıyorsunuz?", section=2, q_type="multiple_choice_multiple")
    Choice.objects.create(question=q_nasil_iliski, text="Ciddi İlişki")
    Choice.objects.create(question=q_nasil_iliski, text="Takılmalık")
    Choice.objects.create(question=q_nasil_iliski, text="Arkadaşlık")
    Question.objects.create(text="Yaş Aralığı", section=2, q_type="number_range")
    Question.objects.create(text="Boy Aralığı", section=2, q_type="number_range")
    q_girlboss = Question.objects.create(text="Girlbossification Scale (Alfa, Omega, Beta)", section=2, q_type="multiple_choice_single")
    Choice.objects.create(question=q_girlboss, text="Alfa")
    Choice.objects.create(question=q_girlboss, text="Omega")
    Choice.objects.create(question=q_girlboss, text="Beta")
    q_samimi = Question.objects.create(text="Samimi Anlarda Değerlendirme Skalası", section=2, q_type="multiple_choice_single")
    Choice.objects.create(question=q_samimi, text="Sub")
    Choice.objects.create(question=q_samimi, text="Dom")
    Choice.objects.create(question=q_samimi, text="Switch")
    Choice.objects.create(question=q_samimi, text="Samimi anlarda bulunmuyorum")
    Question.objects.create(text="Romantiklik Seviyesi (5 Üzerinden)", section=2, q_type="slider", min_value=1, max_value=5)
    Question.objects.create(text="Çekicilik Seviyesi (10 Üzerinden)", section=2, q_type="slider", min_value=1, max_value=10)
    Question.objects.create(text="Dışa Dönüklük Seviyesi (5 Üzerinden)", section=2, q_type="slider", min_value=1, max_value=5)
    Question.objects.create(text="Libido Seviyesi (10 Üzerinden)", section=2, q_type="slider", min_value=1, max_value=10)
    Question.objects.create(text="Aradığın Fiziksel Özellikler", section=2, q_type="open_ended")
    Question.objects.create(text="Aradığın Karakter Özellikleri", section=2, q_type="open_ended")
    Question.objects.create(text="Asla Kabul Etmeyeceğin Özellik ve Davranışlar", section=2, q_type="open_ended")
    Question.objects.create(text="Birisinden Anında Hoşlanmana Sebep Olan Davranışlar", section=2, q_type="open_ended")
    Question.objects.create(text="Red Flagler", section=2, q_type="open_ended")
    q_uzak_mesafe = Question.objects.create(text="Uzak Mesafe Hakkında Görüşün", section=2, q_type="multiple_choice_single")
    Choice.objects.create(question=q_uzak_mesafe, text="Evet")
    Choice.objects.create(question=q_uzak_mesafe, text="Hayır")
    Choice.objects.create(question=q_uzak_mesafe, text="Fark Etmez")
    Question.objects.create(text="Sınırların Neler?", section=2, q_type="open_ended")
    Question.objects.create(text="Hayalindeki Düğün", section=2, q_type="open_ended")
    Question.objects.create(text="Hayalindeki Balayı/Tatil", section=2, q_type="open_ended")

    # Section 3: Geçmiş İlişkiler
    Question.objects.create(text="Son İlişkin Ne Zaman Bitti?", section=3, q_type="open_ended")
    Question.objects.create(text="En Uzun İlişkin Ne Kadar Sürdü?", section=3, q_type="open_ended")
    Question.objects.create(text="Bir Önceki İlişkin Neden Bitti?", section=3, q_type="open_ended")
    Question.objects.create(text="Sonraki İlişkin Ne Kadar Sürsün İstersin?", section=3, q_type="open_ended")

    # Section 4: Ek Bilgiler (Zorunlu Olmayan)
    Question.objects.create(text="Burçlar Hakkında Düşünceler", section=4, q_type="open_ended")
    q_16_personalities = Question.objects.create(text="16 Personalities", section=4, q_type="multiple_choice_single")
    # Adding all 16 personality types as choices
    personality_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]
    for p_type in personality_types:
        Choice.objects.create(question=q_16_personalities, text=p_type)

    q_politik_gorus = Question.objects.create(text="Politik Görüş", section=4, q_type="multiple_choice_single")
    Choice.objects.create(question=q_politik_gorus, text="Sol")
    Choice.objects.create(question=q_politik_gorus, text="Sağ")
    Choice.objects.create(question=q_politik_gorus, text="Merkez")
    q_blacklist_politik = Question.objects.create(text="Blacklist Politik Görüş", section=4, q_type="multiple_choice_multiple")
    Choice.objects.create(question=q_blacklist_politik, text="Liberal")
    Choice.objects.create(question=q_blacklist_politik, text="Sosyalist")
    Choice.objects.create(question=q_blacklist_politik, text="Muhafazakar")
    Choice.objects.create(question=q_blacklist_politik, text="Milliyetçi")
    Question.objects.create(text="Aşk Hayatını Bir Şarkı Sözüyle Tanımla", section=4, q_type="open_ended")
    Question.objects.create(text="İlişki CV'si", section=4, q_type="open_ended")
    Question.objects.create(text="Kendinizi 3. Kişi Ağzından Tanıtan Bir Reklam Yazısı Yazın.", section=4, q_type="open_ended")
    Question.objects.create(text="Eklemek İstediklerin", section=4, q_type="open_ended")

    # Section 5: Eşleşme İpuçları
    Question.objects.create(text="Eşleşmek İstemediğin Kişiler", section=5, q_type="open_ended")
    Question.objects.create(text="Eşleşmek İstediğin Kişiler", section=5, q_type="open_ended")
    Question.objects.create(text="Birkaç Celebrity Crush", section=5, q_type="open_ended")

def remove_questions(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    Question.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_questions, reverse_code=remove_questions),
    ]