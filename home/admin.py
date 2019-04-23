from django.contrib import admin
from .models import Dsaform, Subject
from django.http import HttpResponse
from .createdoc import create_doc
from django.contrib.auth.models import User, Group
from django.contrib import messages


admin.site.unregister(User)
admin.site.unregister(Group)


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 0
    min_num = 1


@admin.register(Dsaform)
class DsaformAdmin(admin.ModelAdmin):

    inlines = [SubjectInline]
    actions = ["download_dsaform"]

    def download_dsaform(self, request, queryset):

        if queryset.__len__() > 1:

            messages.error(request, "Please select only one file to download.")

        else:
            class_no = queryset[0].class_no
            sem_name = queryset[0].sem_name
            teacher_name = queryset[0].teacher_name
            dep_name = queryset[0].dep_name

            sub = Subject.objects.filter(dsaform__teacher_name=teacher_name)

            sub_name = []
            records = ((),)

            sub_len = sub.__len__()
            class_type = 1
            teacher_num = 1
            student_num = 48
            choice = dep_name
            if choice == '0':
                depart_name = 'Electronics and Communication Engineering'
            elif choice == '1':
                depart_name = 'Electronics and Communication Engineering'
            elif choice == '2':
                depart_name = 'Civil Engineering'
            elif choice == '3':
                depart_name = 'Mechanical Engineering'
            elif choice == '4':
                depart_name = 'Electrical Engineering'
            else:
                depart_name = ''

            for i in range(0, sub_len):
                s = sub[i]


                subject = str(s.subject_name)
                period_num = float(s.class_num)
                # choice = s.class_type
                if s.program_name == '3':
                    subject = subject
                else:
                    choice = s.program_name
                    if choice == '0':
                        subject = subject + '[BEX]'
                    elif choice == '1':
                        subject = subject + '[BCT]'
                    elif choice == '2':
                        subject = subject + '[BCE]'
                    elif choice == '3':
                        subject = subject + '[BME]'
                    elif choice == '4':
                        subject = subject + '[BEL]'
                    else:
                        subject = subject

                choice = s.class_type
                if choice == '0':
                    subject = subject + '[L]'
                    class_type = 1
                    teacher_num = 1
                    student_num = 48
                elif choice == '1':
                    subject = subject + '[P]'
                    class_type = 3
                    teacher_num = 3
                    student_num = 24
                elif choice == '2':
                    subject = subject + '[T]'
                    class_type = 1
                    teacher_num = 1
                    student_num = 24
                elif choice == '3':
                    subject = subject
                    class_type = 1
                    teacher_num = 1
                    student_num = 4
                elif choice == '4':
                    subject = subject
                    class_type = 1
                    teacher_num = 1
                    student_num = 3
                else:
                    subject = subject

                sub_name.append(subject)
                sn = str(i + 1)
                result = (sn, str(subject), str(class_type), str(teacher_num), str(period_num), str(student_num))
                records = records + (result,)  # adds the tuple result to the tuple of tuples i.e.  records

            # divide records to two parts and keep latter;
            records = records[1:]  # partition from second element because defining stored empty tuple at first

            file = create_doc(class_no, sem_name, teacher_name, depart_name, records)
            document = file.read()
            # dsaf = Dsauser(userfile_name=dsa.teacher_name.lower(), user_file=File(file))
            # dsa.save()



            # sending response
            response = HttpResponse(document,
                                    content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="dsaform.docx"'
            return response

